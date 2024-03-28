import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Sequence

from pydantic import BaseModel

from server.utils.collect_tools import retrieval_tools
from ..chat import ChatModel
from ..data import Role as DataRole
from ..extras.misc import torch_gc
from ..extras.packages import is_fastapi_availble, is_starlette_available, is_uvicorn_available
from .protocol import (
    ChatCompletionMessage,
    ChatCompletionRequest,
    ToolCallRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionResponseStreamChoice,
    ChatCompletionResponseUsage,
    ChatCompletionStreamResponse,
    Finish,
    Function,
    FunctionCall,
    ModelCard,
    ModelList,
    Role,
    ScoreEvaluationRequest,
    ScoreEvaluationResponse,
    ChatMessage
)

if is_fastapi_availble():
    from fastapi import FastAPI, HTTPException, status
    from fastapi.middleware.cors import CORSMiddleware

if is_starlette_available():
    from sse_starlette import EventSourceResponse

if is_uvicorn_available():
    import uvicorn


@asynccontextmanager
async def lifespan(app: "FastAPI"):  # collects GPU memory
    yield
    torch_gc()


def dictify(data: "BaseModel") -> Dict[str, Any]:
    try:  # pydantic v2
        return data.model_dump(exclude_unset=True)
    except AttributeError:  # pydantic v1
        return data.dict(exclude_unset=True)


def jsonify(data: "BaseModel") -> str:
    try:  # pydantic v2
        return json.dumps(data.model_dump(exclude_unset=True), ensure_ascii=False)
    except AttributeError:  # pydantic v1
        return data.json(exclude_unset=True, ensure_ascii=False)


MAX_RETRIES = 5
RETRY_EXCEPTIONS = HTTPException





def create_app(chat_model: "ChatModel") -> "FastAPI":
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    role_mapping = {
        Role.USER: DataRole.USER.value,
        Role.ASSISTANT: DataRole.ASSISTANT.value,
        Role.SYSTEM: DataRole.SYSTEM.value,
        Role.FUNCTION: DataRole.FUNCTION.value,
        Role.TOOL: DataRole.OBSERVATION.value,
    }

    @app.get("/v1/models", response_model=ModelList)
    async def list_models():
        model_card = ModelCard(id="gpt-3.5-turbo")
        return ModelList(data=[model_card])

    @app.post("/v1/chat/completions", response_model=ChatCompletionResponse, status_code=status.HTTP_200_OK)
    async def create_chat_completion(request: ChatCompletionRequest):
        if not chat_model.engine.can_generate:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Not allowed")

        if len(request.messages) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid length")

        if request.messages[0].role == Role.SYSTEM:
            system = request.messages.pop(0).content
        else:
            system = ""

        if len(request.messages) % 2 == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only supports u/a/u/a/u...")

        input_messages = []
        for i, message in enumerate(request.messages):
            if i % 2 == 0 and message.role not in [Role.USER, Role.TOOL]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
            elif i % 2 == 1 and message.role not in [Role.ASSISTANT, Role.FUNCTION]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

            input_messages.append({"role": role_mapping[message.role], "content": message.content})

        tool_list = request.tools
        if isinstance(tool_list, list) and len(tool_list):
            try:
                tools = json.dumps([tool["function"] for tool in tool_list], ensure_ascii=False)
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid tools")
        else:
            tools = ""

        if request.stream:
            # if tools:
            #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot stream function calls.")

            generate = stream_chat_completion(input_messages, system, tools, request)

            return EventSourceResponse(generate, media_type="text/event-stream")

        responses = await chat_model.achat(
            input_messages,
            system,
            tools,
            do_sample=request.do_sample,
            temperature=request.temperature,
            top_p=request.top_p,
            max_new_tokens=request.max_tokens,
            num_return_sequences=request.n,
        )

        prompt_length, response_length = 0, 0
        choices = []
        for i, response in enumerate(responses):
            if tools:
                result = chat_model.engine.template.format_tools.extract(response.response_text)
            else:
                result = response.response_text

            if isinstance(result, tuple):
                name, arguments = result
                function = Function(name=name, arguments=arguments)
                response_message = ChatCompletionMessage(
                    role=Role.ASSISTANT, tool_calls=[FunctionCall(function=function)]
                )
                finish_reason = Finish.TOOL
            else:
                response_message = ChatCompletionMessage(role=Role.ASSISTANT, content=result)
                finish_reason = Finish.STOP if response.finish_reason == "stop" else Finish.LENGTH

            choices.append(
                ChatCompletionResponseChoice(index=i, message=response_message, finish_reason=finish_reason)
            )
            prompt_length = response.prompt_length
            response_length += response.response_length

        usage = ChatCompletionResponseUsage(
            prompt_tokens=prompt_length,
            completion_tokens=response_length,
            total_tokens=prompt_length + response_length,
        )

        return ChatCompletionResponse(model=request.model, choices=choices, usage=usage)

    async def stream_chat_completion(
            messages: Sequence[Dict[str, str]], system: str, tools: str, request: ChatCompletionRequest
    ):
        choice_data = ChatCompletionResponseStreamChoice(
            index=0, delta=ChatCompletionMessage(role=Role.ASSISTANT, content=""), finish_reason=None
        )
        chunk = ChatCompletionStreamResponse(model=request.model, choices=[choice_data])
        yield jsonify(chunk)

        async for new_token in chat_model.astream_chat(
                messages,
                system,
                tools,
                do_sample=request.do_sample,
                temperature=request.temperature,
                top_p=request.top_p,
                max_new_tokens=request.max_tokens,
        ):
            if len(new_token) == 0:
                continue

            choice_data = ChatCompletionResponseStreamChoice(
                index=0, delta=ChatCompletionMessage(content=new_token), finish_reason=None
            )
            chunk = ChatCompletionStreamResponse(model=request.model, choices=[choice_data])
            yield jsonify(chunk)

        choice_data = ChatCompletionResponseStreamChoice(
            index=0, delta=ChatCompletionMessage(), finish_reason=Finish.STOP
        )
        chunk = ChatCompletionStreamResponse(model=request.model, choices=[choice_data])
        yield jsonify(chunk)
        yield "[DONE]"

    @app.post("/v1/score/evaluation", response_model=ScoreEvaluationResponse, status_code=status.HTTP_200_OK)
    async def create_score_evaluation(request: ScoreEvaluationRequest):
        if chat_model.engine.can_generate:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Not allowed")

        if len(request.messages) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

        scores = await chat_model.aget_scores(request.messages, max_length=request.max_length)
        return ScoreEvaluationResponse(model=request.model, scores=scores)

    async def process_tool_calls(tool_calls, tools_dict, input_messages):
        for tool_call in tool_calls:
            function = tool_call.function
            input_messages.append(ChatMessage(role=Role.ASSISTANT, content=json.dumps(function.dict())))
            tool = tools_dict.get(tool_call.function.name)
            if tool is None:
                raise HTTPException(status_code=404, detail=f"Tool {tool_call.function.name} not found.")

            try:
                tool_response = await tool.arun(dict(json.loads(tool_call.function.arguments)))
                input_messages.append(ChatMessage(role=Role.TOOL, content=tool_response))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # return ChatCompletionResponse(messages=input_messages)

    def create_error_message(exception) -> ChatMessage:
        # 可以选择返回更详细的错误信息
        return ChatMessage(role=Role.OBSERVATION, content=str(exception)[-20:])

    @app.post("/v1/chat/tool/call", response_model=ChatCompletionResponse, status_code=status.HTTP_200_OK)
    async def create_tool_call(request: ToolCallRequest):
        tools_dict, tools_list = retrieval_tools(request)
        input_messages = request.messages
        retries_left = MAX_RETRIES
        prompt_length, response_length = 0, 0
        while retries_left > 0:
            chat_request = ChatCompletionRequest(
                model=request.model,
                messages=input_messages,
                tools=tools_list,
                do_sample=request.do_sample,
                temperature=request.temperature,
                top_p=request.top_p,
                n=request.n,
                max_tokens=request.max_tokens,
                stream=False
            )
            try:
                response = await create_chat_completion(chat_request)
                prompt_length = response.usage.prompt_tokens
                response_length += response.usage.completion_tokens
                message = response.choices[0].message
                tool_calls = message.tool_calls
                if tool_calls:
                    await process_tool_calls(tool_calls, tools_dict, input_messages)
                else:
                    return response
            except RETRY_EXCEPTIONS as e:
                retries_left -= 1
                logging.error(e)
                input_messages.append(ChatMessage(role=Role.OBSERVATION, content=str(e)[-20:]))
                if retries_left == 0:
                    choices = [ChatCompletionResponseChoice(
                        index=0,
                        message=ChatCompletionMessage(role=Role.ASSISTANT, content="Failed after multiple retries."),
                        finish_reason=Finish.STOP)
                    ]
                    usage = ChatCompletionResponseUsage(
                        prompt_tokens=prompt_length,
                        completion_tokens=response_length,
                        total_tokens=prompt_length + response_length,
                    )
                    return ChatCompletionResponse(model=request.model, choices=choices, usage=usage)

    return app


if __name__ == "__main__":
    chat_model = ChatModel()
    app = create_app(chat_model)
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("API_PORT", 8000)), workers=1)
