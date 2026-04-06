import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8 font-sans">
      <header className="max-w-5xl mx-auto mb-12">
        <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">BishopTech Swarm</h1>
        <p className="text-zinc-400 mt-2">Multi-Agent Orchestration Engine</p>
      </header>

      <main className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 hover:border-purple-500 transition-colors">
          <h2 className="text-2xl font-semibold mb-4">Agent Templates</h2>
          <p className="text-zinc-400 mb-6">Create and manage your specialized AI agents using system prompts.</p>
          <Link href="/agents" className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-colors">
            Manage Agents
          </Link>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 hover:border-pink-500 transition-colors">
          <h2 className="text-2xl font-semibold mb-4">Swarms</h2>
          <p className="text-zinc-400 mb-6">Connect agents together into sequential swarms to tackle complex tasks.</p>
          <Link href="/swarms" className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg font-medium transition-colors">
            Build a Swarm
          </Link>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 md:col-span-2">
          <h2 className="text-2xl font-semibold mb-4">Run Execution</h2>
          <p className="text-zinc-400 mb-4">Execute a task using an existing swarm and watch the live execution logs.</p>
          <div className="flex gap-4">
            <input type="text" placeholder="Enter your prompt here..." className="flex-1 bg-black border border-zinc-800 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500" />
            <button className="bg-white text-black px-6 py-2 rounded-lg font-medium hover:bg-zinc-200 transition-colors">Run</button>
          </div>
        </div>

      </main>
    </div>
  );
}