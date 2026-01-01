import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login } from '../api/auth';
import { LogIn, FileText, PresentationChart, Sparkles, Bot } from 'lucide-react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="flex max-w-6xl w-full">
        {/* Project Information Panel */}
        <div className="hidden lg:flex lg:w-1/2 bg-white/10 backdrop-blur-sm rounded-l-lg p-8 flex-col justify-center text-white">
          <div className="mb-8">
            <div className="flex items-center mb-4">
              <Bot className="h-10 w-10 text-yellow-400 mr-3" />
              <h1 className="text-4xl font-bold">AI Document Generator</h1>
            </div>
            <p className="text-xl text-blue-100 mb-6">
              Create professional documents and presentations with the power of AI
            </p>
          </div>

          <div className="space-y-6">
            <div className="flex items-start">
              <div className="bg-blue-400/20 p-3 rounded-lg mr-4">
                <FileText className="h-6 w-6 text-blue-200" />
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Smart Document Creation</h3>
                <p className="text-blue-100">Generate professional Word documents with AI-powered content that matches your requirements perfectly.</p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="bg-purple-400/20 p-3 rounded-lg mr-4">
                <PresentationChart className="h-6 w-6 text-purple-200" />
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Dynamic Presentations</h3>
                <p className="text-blue-100">Create stunning PowerPoint presentations with automated slide generation and professional layouts.</p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="bg-yellow-400/20 p-3 rounded-lg mr-4">
                <Sparkles className="h-6 w-6 text-yellow-200" />
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">AI-Enhanced Content</h3>
                <p className="text-blue-100">Leverage Google Gemini AI for intelligent content generation, refinement, and professional image creation.</p>
              </div>
            </div>
          </div>

          <div className="mt-8 p-4 bg-white/10 rounded-lg">
            <p className="text-sm text-blue-100">
              <strong>✨ New Feature:</strong> Real-time content refinement with custom AI prompts and automatic image generation for presentations.
            </p>
          </div>
        </div>

        {/* Login Form Panel */}
        <div className="w-full lg:w-1/2 bg-white rounded-lg lg:rounded-l-none lg:rounded-r-lg shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4 lg:hidden">
              <Bot className="h-10 w-10 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-800">AI Document Generator</h1>
            </div>
            <div className="flex items-center justify-center mb-4">
              <LogIn className="h-8 w-8 text-blue-600 mr-3" />
              <h2 className="text-2xl font-bold text-gray-800">Welcome Back</h2>
            </div>
            <p className="text-gray-600">Sign in to continue creating amazing documents</p>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <p className="mt-6 text-center text-gray-600">
            Don't have an account?{' '}
            <Link to="/register" className="text-blue-600 hover:text-blue-700 font-medium">
              Register here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
