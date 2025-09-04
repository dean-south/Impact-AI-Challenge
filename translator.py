import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Optional


class T2TT:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the translation service with Google's Gemini model
        
        Args:
            api_key: Google AI API key. If None, will look for GOOGLE_API_KEY env variable
        """
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key


        
        # Initialize the Google Generative AI model (free tier)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,  # Low temperature for more consistent translations
            # convert_system_message_to_human=True
        )
        
        # Create a prompt template for translation
        self.translation_prompt = PromptTemplate(
            input_variables=["source_language", "target_language", "text"],
            template="""
            Translate the following text from {source_language} to {target_language}.
            
            Provide only the translation without any additional explanation or commentary.
            Maintain the original tone, style, and formatting as much as possible.
            
            Text to translate: {text}
            
            Translation:
            """
        )
        
        # Create the translation chain
        self.translation_chain = LLMChain(
            llm=self.llm,
            prompt=self.translation_prompt,
            verbose=False
        )
    
    
    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_language: Source language (e.g., "English", "Spanish", "French")
            target_language: Target language (e.g., "English", "Spanish", "French")
            
        Returns:
            Translated text
        """
        try:
            result = self.translation_chain.run(
                source_language=source_language,
                target_language=target_language,
                text=text
            )
            return result.strip()
        except Exception as e:
            return f"Translation error: {str(e)}"