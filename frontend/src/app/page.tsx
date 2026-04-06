'use client'
import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
  const [activeTab, setActiveTab] = useState('swarms')
  const [prompt, setPrompt] = useState('')
  const [running, setRunning] = useState(false)
  const [runResult, setRunResult] = useState<any>(null)
  const [chatMsg, setChatMsg] = useState('')
  const [chatHistory, setChatHistory] = useState<any[]>([])
  const [useRag, setUseRag] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    if (chatHistory.length > 0) scrollToBottom()
  }, [chatHistory])

  const runSwarm = async () => {
    if (!prompt) return
    setRunning(true)
    // Simulate API call
    setTimeout(() => {
      setRunning(false)
      const mockResult = {
        id: 1,
        status: 'completed',
        final_output: "Based on the multi-agent analysis, the project 'BishopTech Swarm' is set to revolutionize orchestration. It leverages a sequential chain of specialized Gemini instances to process data with high precision. The RAG system ensures that the knowledge base is utilized for contextually accurate responses, and the final synthesis provides a coherent roadmap for implementation."
      }
      setRunResult(mockResult)
      setChatHistory([
        { role: 'assistant', content: mockResult.final_output }
      ])
    }, 2000)
  }

  const sendChat = async () => {
    if (!chatMsg) return
    const userMsg = { role: 'user', content: chatMsg }
    setChatHistory(prev => [...prev, userMsg])
    setChatMsg('')
    
    // Simulate Gemini response
    setTimeout(() => {
      setChatHistory(prev => [...prev, { role: 'assistant', content: 'I am your Gemini assistant. I can help you analyze the swarm output further. Is there anything specific from the result you want to dive into?' }])
    }, 1000)
  }

  return (
    <div className="flex h-screen bg-[#131314] text-[#e3e3e3] font-sans overflow-hidden">
      
      {/* Sidebar */}
      <aside className="w-[280px] bg-[#1e1f20] flex flex-col p-4 border-r border-[#444746] hidden md:flex">
        <div className="flex items-center gap-2 mb-8 px-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 shadow-lg" />
          <span className="text-xl font-medium">BishopTech Swarm</span>
        </div>

        <div className="flex-1 space-y-1">
          <button 
            onClick={() => { setActiveTab('swarms'); setRunResult(null); setChatHistory([]); }} 
            className={`w-full text-left sidebar-item ${activeTab === 'swarms' ? 'active' : ''}`}
          >
            New Swarm
          </button>
          <button 
            onClick={() => setActiveTab('agents')} 
            className={`w-full text-left sidebar-item ${activeTab === 'agents' ? 'active' : ''}`}
          >
            Agent Templates
          </button>
          <button 
            onClick={() => setActiveTab('kb')} 
            className={`w-full text-left sidebar-item ${activeTab === 'kb' ? 'active' : ''}`}
          >
            Knowledge Base
          </button>
        </div>

        <div className="mt-auto border-t border-[#444746] pt-4 px-2 space-y-4">
          <div className="text-xs text-[#9aa0a6] uppercase tracking-wider font-bold">Recent Swarms</div>
          <div className="text-sm text-[#e3e3e3] hover:text-white cursor-pointer truncate">Project Analysis...</div>
          <div className="text-sm text-[#e3e3e3] hover:text-white cursor-pointer truncate">RAG Optimization...</div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col items-center relative h-full">
        
        {/* Scrollable Chat / Content Area */}
        <div className="w-full max-w-[800px] flex-1 overflow-y-auto px-4 pt-8 pb-32 space-y-6">
          
          {!runResult && !running && activeTab === 'swarms' && (
            <div className="h-full flex flex-col justify-center items-center text-center space-y-4">
              <h2 className="text-5xl font-medium text-gemini py-2">Hello, Super Gemini</h2>
              <p className="text-2xl text-[#9aa0a6]">How can I orchestrate your swarm today?</p>
              
              <div className="grid grid-cols-2 gap-4 mt-12 w-full">
                <div className="gemini-card p-6 cursor-pointer hover:bg-[#28292a] transition-colors">
                  <h3 className="font-medium mb-1">Analyze a project</h3>
                  <p className="text-xs text-[#9aa0a6]">Run multiple agents to audit code and docs</p>
                </div>
                <div className="gemini-card p-6 cursor-pointer hover:bg-[#28292a] transition-colors">
                  <h3 className="font-medium mb-1">Brainstorm ideas</h3>
                  <p className="text-xs text-[#9aa0a6]">Let agents generate and critique strategy</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'agents' && (
            <div className="gemini-card p-8 w-full">
              <h2 className="text-3xl font-medium mb-6">Agent Templates</h2>
              <div className="space-y-4">
                <div className="bg-[#28292a] p-4 rounded-xl border border-[#444746] flex justify-between items-center">
                  <div>
                    <h3 className="font-medium">Researcher Agent</h3>
                    <p className="text-sm text-[#9aa0a6]">Specialized in deep data analysis</p>
                  </div>
                  <button className="text-purple-400 text-sm font-medium">Edit</button>
                </div>
                <div className="bg-[#28292a] p-4 rounded-xl border border-[#444746] flex justify-between items-center">
                  <div>
                    <h3 className="font-medium">Synthesis Specialist</h3>
                    <p className="text-sm text-[#9aa0a6]">Final wrapper agent for all swarms</p>
                  </div>
                  <button className="text-purple-400 text-sm font-medium">Edit</button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'kb' && (
            <div className="gemini-card p-8 w-full">
              <h2 className="text-3xl font-medium mb-6">Knowledge Base</h2>
              <div className="border-2 border-dashed border-[#444746] p-12 rounded-2xl text-center hover:border-[#9aa0a6] transition-colors cursor-pointer group">
                <p className="text-[#9aa0a6] group-hover:text-[#e3e3e3]">Drag & drop PDF, TXT or MD files</p>
              </div>
            </div>
          )}

          {running && (
            <div className="flex flex-col items-center justify-center h-full space-y-4">
              <div className="w-12 h-12 rounded-full border-4 border-t-purple-500 border-[#1e1f20] animate-spin" />
              <p className="text-xl text-gemini font-medium animate-pulse">Orchestrating Swarm Agents...</p>
            </div>
          )}

          {chatHistory.map((m, i) => (
            <div key={i} className={m.role === 'user' ? 'gemini-bubble-user' : 'gemini-bubble-ai'}>
              {m.role === 'assistant' && (
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500" />
                  <span className="text-sm font-medium">Gemini Swarm Output</span>
                </div>
              )}
              <div className={`whitespace-pre-wrap leading-relaxed ${m.role === 'assistant' ? 'text-[16px]' : 'text-[14px]'}`}>
                {m.content}
              </div>
              {m.role === 'assistant' && i === 0 && (
                <div className="mt-4 flex gap-2">
                  <button className="text-xs border border-[#444746] px-3 py-1 rounded-full hover:bg-[#28292a]">Export PDF</button>
                  <button className="text-xs border border-[#444746] px-3 py-1 rounded-full hover:bg-[#28292a]">Save to RAG</button>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Floating Input Area */}
        <div className="absolute bottom-8 w-full max-w-[800px] px-4">
          <div className="gemini-input-container p-4 shadow-2xl">
            <div className="flex flex-col gap-2">
              <textarea 
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (runResult ? sendChat() : runSwarm())}
                placeholder={runResult ? "Ask Gemini about this result..." : "Enter a prompt here"} 
                rows={1}
                className="w-full bg-transparent border-none focus:ring-0 text-[#e3e3e3] placeholder-[#9aa0a6] resize-none text-[16px] leading-relaxed max-h-[200px]"
                style={{ height: 'auto' }}
              />
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <button 
                    onClick={() => setUseRag(!useRag)}
                    className={`flex items-center gap-2 text-xs transition-colors ${useRag ? 'text-purple-400' : 'text-[#9aa0a6]'}`}
                  >
                    <div className={`w-3 h-3 rounded-full border ${useRag ? 'bg-purple-500 border-purple-400' : 'border-[#444746]'}`} />
                    Knowledge Base
                  </button>
                  <button className="text-[#9aa0a6] hover:text-white transition-colors">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg>
                  </button>
                </div>
                <button 
                  onClick={runResult ? sendChat : runSwarm}
                  disabled={!prompt || running}
                  className="bg-white text-black w-8 h-8 rounded-full flex items-center justify-center disabled:opacity-30 disabled:cursor-not-allowed hover:bg-[#e3e3e3] transition-colors"
                >
                  <svg className="w-5 h-5 rotate-90" fill="currentColor" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" /></svg>
                </button>
              </div>
            </div>
          </div>
          <p className="text-[11px] text-[#9aa0a6] text-center mt-3">BishopTech Swarm may display inaccurate info, so double-check its responses.</p>
        </div>

      </main>
    </div>
  );
}
