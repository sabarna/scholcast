import json
import re
import networkx as nx
import matplotlib.pyplot as plt
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from networkx.drawing.nx_agraph import graphviz_layout
from pathlib import Path



class PaperAnalyzer:
    def __init__(self, config_path='config/config.json'):
        # Load API keys from configuration
        with open(config_path) as config_file:
            config = json.load(config_file)
        
        # Set up OpenAI API key
        self.OPEN_AI_NARRATION_MODEL = 'gpt-4o-mini'
        self.TEMPERATURE = 0.8
        self.teacher_llm = ChatOpenAI(model_name=self.OPEN_AI_NARRATION_MODEL, temperature=self.TEMPERATURE, openai_api_key=config["openai_api_key"])
        self.student_llm = ChatOpenAI(model_name=self.OPEN_AI_NARRATION_MODEL, temperature=self.TEMPERATURE, openai_api_key=config["openai_api_key"])
        self.overall_narrative = {'teacher':[], 'student':[]}

    def generate_knowledge_graph(self, text):
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Analyze the following academic paper and create a knowledge graph. 
            List the main concepts as nodes and their relationships as edges. 
            Format your response as a list of nodes followed by a list of edges:

            Nodes:
            1. Concept1
            2. Concept2
            ...

            Edges:
            1. Concept1 -> Concept2: Relationship
            2. Concept2 -> Concept3: Relationship
            ...

            Text:
            {text}
            """
        )

        chain = LLMChain(llm=self.teacher_llm, prompt=prompt)
        response = chain.run(text=text)
        return response.strip()

    def generate_explanation(self, graph_text, academic_paper):
        prompt = PromptTemplate(
        input_variables=["graph_text", "academic_paper"],
        template="""Analyze the given academic paper, {academic_paper}, using the provided knowledge graph, 
        {graph_text}, as a guide to navigate through the concepts and structure of the paper. 
        Provide a detailed explanation of the paper's main contributions."""
    )

        chain = LLMChain(llm=self.teacher_llm, prompt=prompt)
        response = chain.run(graph_text=graph_text, academic_paper = academic_paper)
        return response.strip()

    def generate_dialogue(self, overall_narrative):
        ind = 0
        dialogue = ''
        while ind < len(self.overall_narrative['teacher']):
            dialogue += 'Teachers Explanation: '+ self.overall_narrative['teacher'][ind]
            if ind < len(self.overall_narrative['student']):
                dialogue += 'Students Followup: '+ self.overall_narrative['student'][ind]
            ind+=1
        return dialogue

    def generate_student_followup(self, dialogue):
        prompt = PromptTemplate(
        input_variables=["dialogue"],
        template="""The following is an ongoing explanation of a paper. 
        {dialogue}
        You are an undergraduate student aiming to thoroughly understand the 
        content. Then, ask in-depth follow-up questions to clarify any aspects of the latest explanation that are unclear or 
        require further elaboration.""")
        chain = LLMChain(llm=self.student_llm, prompt=prompt)
        response = chain.run(dialogue=dialogue)
        return response.strip()

    def generate_teacher_followup(self, graph_text, academic_paper, dialogue):
        prompt = PromptTemplate(
        input_variables=["graph_text", "academic_paper", "dialogue"],
        template="""YOu are the Teacher. Analyze the following {academic_paper} and use the  knowledge graph {graph_text} to answer the latest 
        questions from the student in detail from the below dialogue:{dialogue} """)
        chain = LLMChain(llm=self.teacher_llm, prompt=prompt)
        response = chain.run(graph_text=graph_text, academic_paper = academic_paper, dialogue = dialogue)
        return response.strip()


    def get_narrative(self, document, title):
        # Generate knowledge graph
        graph_text = self.generate_knowledge_graph(document)
        print(graph_text)
        # Generate explanation
        explanation = self.generate_explanation(graph_text, document)
        intro_text = f"Paper Title : {title}"
        self.overall_narrative['teacher'].append(intro_text + '\n' + explanation)
        dialogue = self.generate_dialogue(self.overall_narrative)
        for i in range(1):
            self.overall_narrative['student'].append(self.generate_student_followup(dialogue))
            dialogue = self.generate_dialogue(self.overall_narrative)
            self.overall_narrative['teacher'].append(self.generate_teacher_followup(graph_text, document, dialogue))
            dialogue = self.generate_dialogue(self.overall_narrative)
        Path('logs').mkdir(parents=True, exist_ok=True)
        with open("logs/narrative.txt", "w") as file:
            file.write(dialogue)
        return self.overall_narrative

    