import { OpenAI } from "https://deno.land/x/openai@v4.69.0/mod.ts";

const openai=new OpenAI({
    apiKey: Deno.env.get("OPENAI_API_KEY"),
});

const response=await openai.images.generate({
    model: "dall-e-2",
    prompt: "",
    n: 1,
    size: "1024x1024",
});

console.log(response.data[0].url);

