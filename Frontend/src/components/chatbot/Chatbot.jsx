import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, User, Bot, Loader2, Trash2 } from 'lucide-react';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';
import { sendChatMessage } from '../../services/chatService';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: 'Hello! I am your AI Logistics Assistant. How can I help you today?',
      sender: 'bot'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!inputValue.trim() || isTyping) return;

    const userText = inputValue.trim();

    const newUserMessage = {
      id: Date.now(),
      text: userText,
      sender: 'user'
    };

    setMessages((prev) => [...prev, newUserMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      const responseText = await sendChatMessage(userText);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: responseText || 'The assistant returned an empty response.',
          sender: 'bot'
        }
      ]);
    } catch (error) {
      console.error('CHATBOT ERROR:', error);

      let errorMessage = 'Unable to connect to the chatbot backend.';

      if (error?.response?.data?.detail) {
        errorMessage = `Backend error: ${error.response.data.detail}`;
      } else if (error?.response?.data?.message) {
        errorMessage = `Backend error: ${error.response.data.message}`;
      } else if (error?.message) {
        errorMessage = `Connection error: ${error.message}`;
      }

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: errorMessage,
          sender: 'bot',
          isError: true
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        text: 'Hello! I am your AI Logistics Assistant. How can I help you today?',
        sender: 'bot'
      }
    ]);
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className={cn(
          'fixed bottom-6 right-6 z-50 p-4 rounded-full shadow-lg transition-all duration-300',
          'bg-cyan-500 hover:bg-cyan-400 text-slate-900',
          isOpen ? 'scale-0 opacity-0' : 'scale-100 opacity-100'
        )}
        aria-label="Open AI Assistant"
      >
        <MessageSquare className="w-6 h-6" />
      </button>

      <div
        className={cn(
          'fixed bottom-6 right-6 z-50 flex flex-col w-[90vw] sm:w-[400px] h-[80vh] sm:h-[600px] max-h-[800px] rounded-2xl shadow-2xl overflow-hidden transition-all duration-300 origin-bottom-right',
          'bg-slate-800 border border-slate-700',
          isOpen
            ? 'scale-100 opacity-100'
            : 'scale-0 opacity-0 pointer-events-none'
        )}
      >
        <div className="flex items-center justify-between p-4 bg-slate-900 border-b border-slate-700">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-cyan-500/20 rounded-lg">
              <Bot className="w-5 h-5 text-cyan-400" />
            </div>

            <div>
              <h3 className="font-semibold text-slate-100">Logistics AI</h3>
              <p className="text-xs text-slate-400">Assistant</p>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={clearChat}
              className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
              title="Clear chat"
            >
              <Trash2 className="w-4 h-4" />
            </button>

            <button
              onClick={() => setIsOpen(false)}
              className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
              title="Close chat"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-800">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={cn(
                'flex items-end gap-2 max-w-[85%]',
                msg.sender === 'user'
                  ? 'ml-auto flex-row-reverse'
                  : 'mr-auto'
              )}
            >
              <div
                className={cn(
                  'flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full',
                  msg.sender === 'user'
                    ? 'bg-slate-700 text-slate-300'
                    : 'bg-cyan-500/20 text-cyan-400'
                )}
              >
                {msg.sender === 'user' ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>

              <div
                className={cn(
                  'px-4 py-2 rounded-2xl text-sm whitespace-pre-wrap shadow-sm',
                  msg.sender === 'user'
                    ? 'bg-cyan-600 text-white rounded-br-none'
                    : msg.isError
                      ? 'bg-red-500/10 text-red-400 border border-red-500/20 rounded-bl-none'
                      : 'bg-slate-700 text-slate-100 rounded-bl-none'
                )}
              >
                {msg.text}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex items-end gap-2 max-w-[85%] mr-auto">
              <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-cyan-500/20 text-cyan-400">
                <Bot className="w-4 h-4" />
              </div>

              <div className="px-4 py-3 rounded-2xl bg-slate-700 text-slate-100 rounded-bl-none shadow-sm flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-cyan-400" />
                <span className="text-xs text-slate-400">
                  AI is thinking...
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 bg-slate-900 border-t border-slate-700">
          <div className="flex items-end gap-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about logistics, routes, or risks..."
              className="flex-1 max-h-32 min-h-[44px] p-3 bg-slate-800 border border-slate-700 rounded-xl text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 resize-none transition-all"
              rows={1}
            />

            <button
              onClick={handleSend}
              disabled={!inputValue.trim() || isTyping}
              className="p-3 bg-cyan-500 hover:bg-cyan-400 text-slate-900 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </>
  );
}