import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User } from 'lucide-react';
import { translations } from '../translations';
import './ChatArea.css';

const ChatArea = ({ messages, input, setInput, onSendMessage, isLoading, language }) => {
    const messagesEndRef = useRef(null);
    const t = translations[language].chat;

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSendMessage();
        }
    };

    return (
        <div className="chat-container">
            <div className="messages-list">
                {messages.length === 0 ? (
                    <div className="empty-state">
                        <div className="empty-logo">
                            <Bot size={48} />
                        </div>
                        <h2>{t.welcome}</h2>
                        <p className="subtitle"></p>
                    </div>
                ) : (
                    messages.map((msg, index) => (
                        <div key={index} className={`message-wrapper ${msg.sender}`}>
                            <div className="message-avatar">
                                {msg.sender === 'bot' ? <Bot size={20} /> : <User size={20} />}
                            </div>
                            <div className={`message-bubble ${msg.sender}`}>
                                {msg.sender === 'bot' ? (
                                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                                ) : (
                                    msg.text
                                )}
                            </div>
                        </div>
                    ))
                )}

                {isLoading && (
                    <div className="message-wrapper bot">
                        <div className="message-avatar">
                            <Bot size={20} />
                        </div>
                        <div className="message-bubble bot loading">
                            <div className="typing-dot"></div>
                            <div className="typing-dot"></div>
                            <div className="typing-dot"></div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                <div className="input-wrapper">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={t.placeholder}
                        rows={1}
                        className="chat-input"
                    />
                    <button
                        className="send-btn"
                        onClick={onSendMessage}
                        disabled={!input.trim() || isLoading}
                    >
                        <Send size={20} />
                    </button>
                </div>
                <div className="disclaimer">
                    copyright © 2026 <a href="https://www.github.com/tetherium" target="_blank" rel="noopener noreferrer">Tetherium</a>.
                </div>
            </div>
        </div>
    );
};

export default ChatArea;
