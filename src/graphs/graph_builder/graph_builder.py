from langgraph.graph import StateGraph,START,END,MessagesState
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic
        """
        self.blog_node = BlogNode(self.llm)
        ##Nodes
        self.graph.add_node("title_creation",self.blog_node.title_creation)
        self.graph.add_node("content_generation",self.blog_node.content_generator)
        
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation",END)

        return self.graph
    def build_language_graph(self):
        """ 
        Build a graph for blog generation with inputs topics and language
        """
        self.blog_node = BlogNode(self.llm)
        ##Nodes
        self.graph.add_node("title_creation",self.blog_node.title_creation)
        self.graph.add_node("content_generation",self.blog_node.content_generator)
        self.graph.add_node("irish_translation",lambda state: self.blog_node.translation({**state, "current_language":"irish"}))
        self.graph.add_node("tamil_translation",lambda state: self.blog_node.translation({**state, "current_language":"tamil"}))
        self.graph.add_node("route",self.blog_node.route)

        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation","route")       

        self.graph.add_conditional_edges(
            "route",
            self.blog_node.route_decision,
            {
                "irish":"irish_translation",
                "tamil":"tamil_translation"
            }
        )
        self.graph.add_edge("irish_translation",END)
        self.graph.add_edge("tamil_translation",END)
        return self.graph
    
    def setup_graph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()
        if usecase == "language":
            self.build_language_graph()  
        return self.graph.compile()
    
    #langsmith studio

llm = GroqLLM().get_llm()

graph_builder = GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()