# AI Pipe OpenAI-Compatible Proxy (Railway)

Public endpoint:
`https://YOUR-RAILWAY-DOMAIN/v1/chat/completions`

## Railway variables
Set these under Service → Variables:
- `AIPIPE_TOKEN` = your AI Pipe token (keep it secret)
- `AIPIPE_MODEL` = `openai/gpt-4.1-nano` (optional)

The service accepts OpenAI-compatible JSON requests and forwards them to
`https://aipipe.org/openrouter/v1/chat/completions`. It forces `stream=false`
so the grader receives a standard JSON response. CORS is enabled.

## Deploy
1. Upload the repository contents to a GitHub repository.
2. In Railway, create a project from that GitHub repo.
3. Add the environment variable `AIPIPE_TOKEN`.
4. Generate a public domain.
5. Test `/healthz` and `POST /v1/chat/completions`.

Note: this proxies a hosted model; it is not a local Ollama instance.
