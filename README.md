# ReAct Agent with RAG + Tools + Memory

This Python application combines the ReAct (Reasoning and Acting) pattern with Retrieval-Augmented Generation (RAG) capabilities. It creates an intelligent agent that can reason through problems, use multiple tools including a company knowledge base search, and maintain conversation memory.

## Overview

This advanced implementation extends the basic ReAct pattern by integrating:
- **RAG Capabilities**: Search and retrieve information from indexed company documents
- **Multiple Tools**: Wikipedia, datetime, and internal knowledge base access
- **Smart Memory**: Conversation summarization with recent message retention
- **Azure Integration**: Full Azure OpenAI and Azure Cognitive Search integration

The agent can handle complex queries by combining public knowledge (Wikipedia) with private company data (Azure Search) while maintaining context across conversations.

## Features

- 🧠 **ReAct Pattern**: Structured reasoning and acting in iterative cycles
- 📚 **RAG Integration**: Search company documents with Azure Cognitive Search
- 🛠️ **Multi-Tool Support**: Wikipedia, datetime, and knowledge base tools
- 💾 **Intelligent Memory**: Hybrid memory system with summarization
- ⚡ **Async Processing**: Non-blocking execution for better performance
- 🔒 **Enterprise Ready**: Secure access to internal company documents
- 🔄 **Error Recovery**: Robust error handling and parsing recovery
- 🎯 **Interactive Chat**: Continuous conversation with context awareness

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI service instance
- Azure Cognitive Search service with indexed documents
- Valid API keys and proper service configuration
- Internet connection for Wikipedia tool

## Required Dependencies

```bash
pip install langchain langchain-openai python-dotenv wikipedia openai
```

## Environment Setup

Create a `.env` file in the same directory as the script:

```env
# Azure OpenAI Configuration
AZURE_OAI_ENDPOINT=https://your-openai-endpoint.openai.azure.com/
AZURE_OAI_KEY=your-openai-api-key
AZURE_OAI_DEPLOYMENT=gpt-4o

# Azure Cognitive Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-name.search.windows.net/
AZURE_SEARCH_KEY=your-search-admin-key
AZURE_SEARCH_INDEX=margies-index
```

## Usage

### Running the Application

1. Ensure all environment variables are properly configured
2. Verify your Azure Cognitive Search index contains documents
3. Install the required dependencies
4. Run the application:

```bash
python React+RAG.py
```

### Interacting with the Agent

The agent will prompt you to ask questions. You can:
- Ask about company-specific information (uses RAG)
- Ask factual questions (uses Wikipedia)
- Ask for current date/time
- Ask complex questions requiring multiple tools
- Type 'quit' to exit

### Example Interactions

```bash
🤖 ReAct Agent with RAG + Tools + Memory (LangChain + Azure OpenAI)

Ask something (or 'quit'): What are our company's vacation policies?

[Agent uses Company Knowledge Base to search internal documents]

Ask something (or 'quit'): What's today's date and who founded Microsoft?

[Agent uses DateTime tool, then Wikipedia for Microsoft information]

Ask something (or 'quit'): How does our leave policy compare to industry standards?

[Agent combines company knowledge with external research]
```

## Architecture

### Available Tools

1. **Date Time Tool**
   - Function: `get_current_datetime()`
   - Purpose: Returns current date and time in ISO format
   - Use case: Time-sensitive queries and date references

2. **Wikipedia Tool**
   - Function: `get_wikipedia_summary(query)`
   - Purpose: Retrieves Wikipedia article summaries
   - Error handling: Manages disambiguation and page errors
   - Use case: General knowledge and public information

3. **Company Knowledge Base Tool**
   - Function: `search_company_docs(query)`
   - Purpose: Searches indexed company documents using Azure Cognitive Search
   - Integration: Full RAG implementation with Azure Search
   - Use case: Internal company information, policies, procedures

### RAG Implementation

The Company Knowledge Base tool implements a complete RAG pipeline:

1. **Query Processing**: Receives natural language questions
2. **Document Retrieval**: Uses Azure Cognitive Search to find relevant documents
3. **Context Integration**: Provides retrieved documents as context to the LLM
4. **Answer Generation**: Generates responses grounded in company data
5. **Response Delivery**: Returns contextually relevant answers

### Memory System

Uses `ConversationSummaryBufferMemory` providing:
- **Recent Messages**: Keeps last 10 interactions for immediate context
- **Conversation Summary**: Summarizes older conversations (150 tokens)
- **Context Continuity**: Maintains thread across complex multi-turn conversations

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OAI_ENDPOINT` | Azure OpenAI service endpoint | `https://myopenai.openai.azure.com/` |
| `AZURE_OAI_KEY` | Azure OpenAI API key | `your-api-key-here` |
| `AZURE_OAI_DEPLOYMENT` | Model deployment name | `gpt-4o` |
| `AZURE_SEARCH_ENDPOINT` | Azure Search service endpoint | `https://mysearch.search.windows.net/` |
| `AZURE_SEARCH_KEY` | Azure Search admin key | `your-search-key` |
| `AZURE_SEARCH_INDEX` | Search index name | `company-docs` |

### Customizable Parameters

```python
# Memory configuration
max_token_limit=150,    # Summary size
k=10                   # Recent messages to keep

# LLM configuration
temperature=0,         # Response consistency (0 = deterministic)
api_version="2024-02-01"  # Azure OpenAI API version

# Agent configuration
verbose=True,          # Show reasoning steps
handle_parsing_errors=True  # Auto-recover from errors
```

## Tool Integration Details

### RAG Tool Implementation

The `search_company_docs` function:
- Creates Azure OpenAI client with search integration
- Uses `extra_body` parameter for data source configuration
- Implements proper error handling for search failures
- Returns grounded answers based on indexed documents

### Error Handling

Each tool includes comprehensive error management:
- **Wikipedia**: Handles disambiguation and missing pages
- **Company Search**: Manages authentication and search errors
- **DateTime**: Robust timestamp generation

## Advanced Features

### Multi-Tool Reasoning

The agent can combine multiple tools in a single response:
```
User: "What's our current remote work policy and how does it compare to Google's?"

Agent reasoning:
1. Use Company Knowledge Base → Get internal remote work policy
2. Use Wikipedia → Research Google's remote work approach  
3. Compare and synthesize information
```

### Context-Aware Conversations

Memory system enables follow-up questions:
```
User: "What are our benefits?"
Agent: [Searches company docs for benefits information]

User: "How do they compare to industry standards?"
Agent: [Remembers previous context about benefits, searches for comparisons]
```

## Troubleshooting

### Common Issues

1. **RAG Tool Not Working**
   - Verify Azure Search endpoint and key
   - Check if search index exists and contains documents
   - Ensure proper authentication configuration

2. **Agent Not Using Correct Tool**
   - Review tool descriptions for clarity
   - Check if query matches tool capabilities
   - Verify prompt template is loaded correctly

3. **Memory Issues**
   - Reduce `max_token_limit` if conversations get too long
   - Adjust `k` value for optimal recent message retention
   - Ensure `return_messages=True` is set

4. **Search Results Poor Quality**
   - Review document indexing in Azure Search
   - Check search index configuration
   - Verify document content is properly processed

### Debug Mode

Enable detailed logging to see agent reasoning:

```python
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,  # Shows detailed reasoning steps
    handle_parsing_errors=True,
)
```

## Security Considerations

- Store all API keys in environment variables
- Use Azure Key Vault for production deployments
- Implement proper access controls for company documents
- Regular key rotation and monitoring
- Consider using managed identities in Azure

## Performance Optimization

### Async Benefits
- Non-blocking tool execution
- Better resource utilization
- Improved user experience

### Memory Efficiency
- Automatic conversation summarization
- Token limit management
- Optimal context window usage

### Search Optimization
- Index relevant documents only
- Use appropriate search configurations
- Implement caching for frequent queries

## Sample Output

```
🤖 ReAct Agent with RAG + Tools + Memory (LangChain + Azure OpenAI)

Ask something (or 'quit'): What's our vacation policy and what's today's date?

> Entering new AgentExecutor chain...
I need to get information about the company's vacation policy and today's date.

Action: Date Time
Action Input: 

Observation: 2025-07-16T14:30:25.123456
Thought: Now I have today's date. Let me search for the company's vacation policy.

Action: Company Knowledge Base
Action Input: vacation policy employee time off

Observation: According to the employee handbook, our vacation policy provides...

Thought: I now have both pieces of information requested.

Final Answer: Today's date is July 16, 2025. Our company's vacation policy...

📣 Response:
Today's date is July 16, 2025. Our company's vacation policy...
```

## File Structure

```
.
├── React+RAG.py           # Main application file
├── React_RAG_README.md    # This documentation
└── .env                  # Environment variables (create this file)
```

## Customization Examples

### Adding New Tools

```python
def calculate_numbers(expression):
    """Safe calculator for basic math"""
    try:
        return str(eval(expression))  # Use safer alternatives in production
    except:
        return "Invalid calculation"

tools.append(
    Tool(
        name="Calculator",
        func=calculate_numbers,
        description="Perform basic mathematical calculations."
    )
)
```

### Custom RAG Implementation

```python
def search_specific_database(query):
    """Search a specific database or API"""
    # Your custom search implementation
    return search_results

tools.append(
    Tool(
        name="Product Database",
        func=search_specific_database,
        description="Search our product catalog and specifications."
    )
)
```

## Dependencies Details

- **langchain**: Core LLM application framework
- **langchain-openai**: Azure OpenAI integration
- **python-dotenv**: Environment variable management
- **wikipedia**: Wikipedia API access
- **openai**: Direct Azure OpenAI client for RAG

## Next Steps

Consider enhancing with:
- **Additional RAG Sources**: Multiple knowledge bases
- **Custom Prompt Templates**: Domain-specific reasoning
- **Web Interface**: Streamlit or FastAPI frontend
- **Analytics**: Conversation tracking and insights
- **Multi-Modal**: Image and document processing
- **Workflow Integration**: Teams, Slack, or email
- **Advanced Search**: Semantic search improvements

## Support

For assistance with:
- **LangChain**: [LangChain Documentation](https://python.langchain.com/)
- **Azure OpenAI**: [Azure OpenAI Documentation](https://docs.microsoft.com/azure/cognitive-services/openai/)
- **Azure Search**: [Azure Cognitive Search Documentation](https://docs.microsoft.com/azure/search/)
- **ReAct Pattern**: [Original ReAct Paper](https://arxiv.org/abs/2210.03629)

## License

This project is provided for educational and demonstration purposes.
