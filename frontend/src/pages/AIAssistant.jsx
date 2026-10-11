import React, { useState, useRef, useEffect } from 'react';
import { 
  BotMessageSquare, Send, User, Sparkles, 
  RotateCcw, ShieldCheck, ArrowRight, HelpCircle 
} from 'lucide-react';
import api from '../services/api';

export default function AIAssistant({ t, lang }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: lang === 'mr'
        ? 'नमस्कार! मी तुमचा **अॅग्रीस्मार्ट (AgriSmart) कृषी सहाय्यक** आहे. मिरचीवरील रोग (बोकड्या, जिवाणू ठिपके, भुरी रोग), माती आरोग्य, NPK खते आणि स्मार्ट सिंचनाबद्दल तुम्ही मला मराठी किंवा इंग्रजीत विचारू शकता.'
        : 'Hello! I am your **AgriSmart AI Agricultural Assistant**. You can ask me anything about Chilli diseases (Leaf Curl Virus, Bacterial Spot, Powdery Mildew), Soil NPK balancing, precision irrigation scheduling, or weather precautions.'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(
    lang === 'mr'
      ? [
          'मिरचीवरील बोकड्या रोगावर काय उपाय करावा?',
          'मिरचीसाठी खतांचे योग्य व्यवस्थापन कसे करावे?',
          'जमिनीचा सामू (pH) कसा सुधारावा?',
          'ठिबक सिंचनाने पाणी कधी द्यावे?'
        ]
      : [
          'How to treat Chilli Leaf Curl Virus?',
          'What is the ideal soil pH and NPK for chilli?',
          'How to cure powdery mildew on chilli leaves?',
          'What is the best irrigation schedule for chilli?'
        ]
  );

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText) => {
    const text = queryText || input;
    if (!text.trim() || loading) return;

    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.sendChatMessage({
        message: text,
        language: lang,
        conversation_history: messages.slice(-6)
      });

      const assistantMsg = {
        role: 'assistant',
        content: res.data.reply
      };
      setMessages((prev) => [...prev, assistantMsg]);
      if (res.data.suggested_questions && res.data.suggested_questions.length > 0) {
        setSuggestions(res.data.suggested_questions);
      }
    } catch (err) {
      console.error('Chat assistant error:', err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an issue retrieving agricultural guidance. Please ensure the backend is running.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: lang === 'mr'
          ? 'मी सज्ज आहे! कृपया तुमचा प्रश्न विचारा.'
          : 'I am ready! Please ask your agricultural question.'
      }
    ]);
  };

  return (
    <div className="space-y-4 max-w-4xl mx-auto flex flex-col h-[calc(100vh-8rem)]">
      
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight sm:text-3xl flex items-center gap-2.5">
            <BotMessageSquare className="h-7 w-7 text-emerald-400" />
            <span>{t.assistant.title}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            {t.assistant.subtitle}
          </p>
        </div>

        <button
          onClick={clearChat}
          className="flex items-center gap-1.5 rounded-xl border border-slate-800 bg-slate-900 px-3 py-1.5 text-xs text-slate-400 hover:text-white transition-all"
        >
          <RotateCcw className="h-3 w-3" />
          <span>Clear</span>
        </button>
      </div>

      {/* Messages Scroll Area */}
      <div className="agri-card flex-1 p-4 sm:p-6 overflow-y-auto space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${
              msg.role === 'user' ? 'flex-row-reverse' : ''
            }`}
          >
            {/* Avatar */}
            <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
              msg.role === 'user'
                ? 'bg-emerald-600 text-white'
                : 'bg-gradient-to-br from-emerald-500/20 to-teal-500/10 text-emerald-400 border border-emerald-500/30'
            }`}>
              {msg.role === 'user' ? <User className="h-4 w-4" /> : <BotMessageSquare className="h-4 w-4" />}
            </div>

            {/* Bubble */}
            <div className={`max-w-[85%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed whitespace-pre-line ${
              msg.role === 'user'
                ? 'bg-emerald-600 text-white rounded-tr-none'
                : 'bg-slate-950/80 text-slate-200 border border-slate-800 rounded-tl-none'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-start gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-emerald-400 border border-slate-800">
              <BotMessageSquare className="h-4 w-4" />
            </div>
            <div className="rounded-2xl rounded-tl-none bg-slate-950 p-4 border border-slate-800 flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Questions */}
      {suggestions.length > 0 && (
        <div className="space-y-1.5">
          <span className="text-[11px] font-semibold text-slate-400 block px-1">
            {t.assistant.suggestedTitle}
          </span>
          <div className="flex flex-wrap gap-1.5">
            {suggestions.map((sq, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(sq)}
                className="rounded-xl border border-slate-800 bg-slate-900/80 px-3 py-1.5 text-xs text-slate-300 hover:border-emerald-500/50 hover:bg-emerald-950/20 hover:text-emerald-300 transition-all text-left"
              >
                {sq}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Box */}
      <form
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        className="flex items-center gap-2 bg-slate-900 p-1.5 rounded-2xl border border-slate-800"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t.assistant.inputPlaceholder}
          className="flex-1 bg-transparent px-4 py-2.5 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-600 text-white hover:bg-emerald-500 transition-all disabled:opacity-40 disabled:hover:bg-emerald-600"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>

    </div>
  );
}
