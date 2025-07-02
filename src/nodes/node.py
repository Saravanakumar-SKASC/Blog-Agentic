from src.states.blogstate import BlogState
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from src.states.blogstate import Blog

class BlogNode:
    """ 
    A class to represent the blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """ 
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt= """
                    You are an expert blog content writer. Use Markdown formatting. Generate a blog title for the {topic}
                    This title should be creative and SEO friendly
                    """
            
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":response.content}}
        
    def content_generator(self, state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt =  """You are expert blog writer. Use Markdown formatting. Generate a detiled blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":state['blog']['title'], "content":response.content}}
        
    def translation(self, state: dict):
        blog = state["blog"]
        # Option 1 (dict)
        blog_title = blog["title"]
        blog_content = blog["content"]
        language = state["current_language"]

        prompt = f"""
    Translate the blog post into {language}. Return only JSON with `title` and `content`.

    Original Title:
    {blog_title}

    Original Content:
    {blog_content}
    """

        messages = [HumanMessage(content=prompt)]
        translated_blog: Blog = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": translated_blog}

    def route(self, state: BlogState):
        return {"current_language": state['current_language'] }
    



    def route(self,state:BlogState):
        return {"current_language": state['current_language'].lower()}
    
    def route_decision(self, state:BlogState):
        """ 
        Route the content to the respective translation function
        """

        if state["current_language"] == "irish":
            return "irish"
        elif state["current_language"] == "tamil":
            return "tamil"
        else:
            return state["current_language"]