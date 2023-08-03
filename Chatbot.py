import os
import replicate

class LLMChatBot:
    def __init__(self, api_token):
        os.environ["REPLICATE_API_TOKEN"] = api_token

    def generate_response(self, pre_prompt, prompt_input, temperature=0.5, top_p=0.6, max_length=160, repetition_penalty=1):
        full_response = ""

        # Generate LLM response
        output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',  # LLM model
                               input={"prompt": f"{pre_prompt} {prompt_input} Assistant: ",  # Prompts
                                      "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": repetition_penalty})  # Model parameters

        for item in output:
            full_response += item

        return full_response

if __name__ == "__main__":
    api_token = "r8_Cb06Mjr3LNnlc0Cnamkp6N4sW0utmwF4ShBOK"
    pre_prompt = "You reply by the name of Assistant. You will reply directly with an answer. You are a very clickbait person that wants to go viral."
    prompt_input = "Reply with a very realistic Tik-Tok video description and a lot of hashtacks about this topic: #viral.It needs to go viral. Assistant:"
    
    bot = LLMChatBot(api_token)
    response = bot.generate_response(pre_prompt, prompt_input, temperature=0.5, top_p=0.6, max_length=160, repetition_penalty=1)
    print(response)
