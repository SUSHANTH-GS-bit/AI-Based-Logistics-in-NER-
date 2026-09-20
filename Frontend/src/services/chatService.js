/**
 * Chat service for the AI Logistics Assistant.
 * Uses the existing project API client (axios instance) from api.js,
 * which reads the backend base URL from VITE_API_BASE_URL env var.
 *
 * Backend endpoint: POST /api/chat
 * Request:  { message: string, context?: object }
 * Response: { reply: string }
 *
 * No API keys are exposed here — all AI calls happen server-side.
 */
import apiClient from './api';

/**
 * Send a user message to the backend AI chat endpoint.
 *
 * @param {string} message - The user's question.
 * @param {object|null} context - Optional dashboard context (page, risks, etc.).
 * @returns {Promise<string>} The AI's reply text.
 */
export async function sendChatMessage(message, context = null) {
  const payload = { message };
  if (context && typeof context === 'object') {
    payload.context = context;
  }

  const response = await apiClient.post('/api/chat', payload);
  return response.data.reply;
}
