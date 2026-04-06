'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
  const [activeTab, setActiveTab] = useState('swarms')
  const [prompt, setPrompt] = useState('')
  const [running, setRunning] = useState(false)
  const [runResult, setRunResult] = useState<any>(null)
  const [chatMsg, setChatMsg] = useState('')
  const [chatHistory, setChatHistory] = useState<any[]>([])

  const runSwarm = async () => {
    setRunning(true)
    // For demo purposes, we'd call /api/swarms/1/run
    // Let's assume the run starts and we poll
    setRunning(false)
    setRunResult({
      id: 1,
      status: 'completed',
      final_output: 'This is a sample output from the swarm. It successfully analyzed the complex question using multiple agents.'
    })
  }

  const sendChat = async () => {
    if (!chatMsg) return
    const newMsg = { role: 'user', content: chatMsg }
    setChatHistory([...chatHistory, newMsg])
    setChatMsg('')

    // In reality: await fetch(`/api/runs/${runResult.id}/chat`, { method: 'POST', body: JSON.stringify({ message: chatMsg }) })
    setTimeout(() => {
      setChatHistory(prev => [...prev, { role: 'assistant', content: 'I am the Gemini-powered chat assistant. I have reviewed the swarm output and can answer your questions about it.' }])
    }, 1000)
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8 font-sans">
      <header className="max-w-5xl mx-auto mb-12 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">BishopTech Swarm</h1>
          <p className="text-zinc-400 mt-2">Multi-Agent Orchestration Engine</p>
        </div>
        <nav className="flex gap-4">
          <button onClick={() => setActiveTab('swarms')} className={`px-4 py-2 rounded-lg ${activeTab === 'swarms' ? 'bg-zinc-800 text-white' : 'text-zinc-500'}`}>Swarms</button>
          <button onClick={() => setActiveTab('kb')} className={`px-4 py-2 rounded-lg ${activeTab === 'kb' ? 'bg-zinc-800 text-white' : 'text-zinc-500'}`}>Knowledge Base</button>
        </nav>
      </header>

      <main className="max-w-5xl mx-auto space-y-8">

        {activeTab === 'swarms' && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 hover:border-purple-500 transition-colors">
                <h2 className="text-2xl font-semibold mb-4">Agent Templates</h2>
                <p className="text-zinc-400 mb-6">Create and manage your specialized AI agents using system prompts.</p>
                <Link href="/agents" className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-colors">
                  Manage Agents
                </Link>
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 hover:border-pink-500 transition-colors">
                <h2 className="text-2xl font-semibold mb-4">Swarm Builder</h2>
                <p className="text-zinc-400 mb-6">Connect agents together into sequential swarms to tackle complex tasks.</p>
                <Link href="/swarms" className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg font-medium transition-colors">
                  Build a Swarm
                </Link>
              </div>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <h2 className="text-2xl font-semibold mb-4">Run Execution</h2>
              <div className="flex flex-col gap-4">
                <textarea 
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Enter your complex task here..." 
                  className="w-full bg-black border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-purple-500 min-h-[100px]" 
                />
                <div className="flex items-center gap-4">
                  <label className="flex items-center gap-2 text-zinc-400">
                    <input type="checkbox" className="accent-purple-500" /> Use RAG Knowledge Base
                  </label>
                  <select className="bg-zinc-800 border border-zinc-700 rounded px-2 py-1 text-sm text-white">
                    <option>Select KB...</option>
                    <option>Company Docs</option>
                  </select>
                  <button 
                    onClick={runSwarm}
                    disabled={running}
                    className="ml-auto bg-white text-black px-8 py-2 rounded-lg font-bold hover:bg-zinc-200 transition-colors disabled:opacity-50"
                  >
                    {running ? 'Processing Swarm...' : 'Execute Swarm'}
                  </button>
                </div>
              </div>
            </div>

            {runResult && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="md:col-span-2 bg-zinc-900 border border-zinc-800 rounded-xl p-6">
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-2xl font-semibold">Swarm Output</h2>
                    <div className="flex gap-2">
                      <button className="bg-zinc-800 hover:bg-zinc-700 text-xs px-3 py-1 rounded text-zinc-300">Export PDF</button>
                      <button className="bg-zinc-800 hover:bg-zinc-700 text-xs px-3 py-1 rounded text-zinc-300">Sync to RAG</button>
                    </div>
                  </div>
                  <div className="bg-black p-4 rounded-lg border border-zinc-800 text-zinc-300 whitespace-pre-wrap">
                    {runResult.final_output}
                  </div>
                </div>

                <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 flex flex-col h-[500px]">
                  <h2 className="text-xl font-semibold mb-4">Chat with Output</h2>
                  <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
                    {chatHistory.map((m, i) => (
                      <div key={i} className={`p-3 rounded-lg text-sm ${m.role === 'user' ? 'bg-purple-900/30 ml-4 border border-purple-800/50' : 'bg-zinc-800 mr-4 border border-zinc-700'}`}>
                        <span className="text-[10px] uppercase font-bold text-zinc-500 block mb-1">{m.role}</span>
                        {m.content}
                      </div>
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <input 
                      type="text" 
                      value={chatMsg}
                      onChange={(e) => setChatMsg(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && sendChat()}
                      placeholder="Ask about result..." 
                      className="flex-1 bg-black border border-zinc-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-purple-500" 
                    />
                    <button onClick={sendChat} className="bg-white text-black px-4 py-2 rounded-lg text-sm font-bold">Send</button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {activeTab === 'kb' && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
            <h2 className="text-2xl font-semibold mb-4">Knowledge Base Management</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-black border border-zinc-800 p-4 rounded-lg">
                <h3 className="font-bold mb-2">Create New KB</h3>
                <input type="text" placeholder="Name" className="w-full bg-zinc-900 border border-zinc-800 rounded px-3 py-2 text-sm mb-2" />
                <button className="w-full bg-purple-600 py-2 rounded text-sm font-bold">Create</button>
              </div>
              <div className="md:col-span-2 bg-black border border-zinc-800 p-4 rounded-lg">
                <h3 className="font-bold mb-4">Documents</h3>
                <div className="border border-dashed border-zinc-700 p-8 rounded-lg text-center text-zinc-500 hover:border-zinc-500 transition-colors cursor-pointer">
                  Drag & Drop Files Here (.pdf, .txt, .md)
                </div>
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}