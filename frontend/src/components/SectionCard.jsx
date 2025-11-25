import { useState } from 'react';
import { ThumbsUp, ThumbsDown, MessageSquare, Sparkles, RefreshCw } from 'lucide-react';
import { generateContent, refineContent, addFeedback, addComment } from '../api/llm';

export default function SectionCard({ section, onUpdate }) {
  const [loading, setLoading] = useState(false);
  const [refinePrompt, setRefinePrompt] = useState('');
  const [showRefine, setShowRefine] = useState(false);
  const [comment, setComment] = useState('');
  const [showComments, setShowComments] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateContent(section.id);
      onUpdate();
    } catch (error) {
      alert('Failed to generate content: ' + error.message);
    }
    setLoading(false);
  };

  const handleRefine = async () => {
    if (!refinePrompt.trim()) return;
    
    setLoading(true);
    try {
      await refineContent(section.id, refinePrompt);
      setRefinePrompt('');
      setShowRefine(false);
      onUpdate();
    } catch (error) {
      alert('Failed to refine content: ' + error.message);
    }
    setLoading(false);
  };

  const handleFeedback = async (isLiked) => {
    try {
      await addFeedback(section.id, isLiked);
      alert('Feedback recorded!');
    } catch (error) {
      alert('Failed to add feedback: ' + error.message);
    }
  };

  const handleAddComment = async () => {
    if (!comment.trim()) return;
    
    try {
      await addComment(section.id, comment);
      setComment('');
      alert('Comment added!');
    } catch (error) {
      alert('Failed to add comment: ' + error.message);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold text-gray-800">{section.title}</h3>
        <div className="flex space-x-2">
          {!section.content && (
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 font-semibold transition-all"
            >
              <Sparkles className="h-5 w-5" />
              <span>{loading ? 'Generating...' : 'Generate Content'}</span>
            </button>
          )}
          {section.content && (
            <button
              onClick={() => setShowRefine(!showRefine)}
              className="flex items-center space-x-1 bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Refine</span>
            </button>
          )}
        </div>
      </div>

      {section.content && (
        <>
          <div className="prose max-w-none mb-4">
            <p className="text-gray-700 leading-relaxed">{section.content}</p>
          </div>

          <div className="flex items-center space-x-4 border-t pt-4">
            <button
              onClick={() => handleFeedback(true)}
              className="flex items-center space-x-1 text-green-600 hover:text-green-700"
            >
              <ThumbsUp className="h-5 w-5" />
              <span>Like</span>
            </button>
            <button
              onClick={() => handleFeedback(false)}
              className="flex items-center space-x-1 text-red-600 hover:text-red-700"
            >
              <ThumbsDown className="h-5 w-5" />
              <span>Dislike</span>
            </button>
            <button
              onClick={() => setShowComments(!showComments)}
              className="flex items-center space-x-1 text-blue-600 hover:text-blue-700"
            >
              <MessageSquare className="h-5 w-5" />
              <span>Comment</span>
            </button>
          </div>

          {showRefine && (
            <div className="mt-4 p-4 bg-purple-50 rounded">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                How would you like to refine this content?
              </label>
              <textarea
                value={refinePrompt}
                onChange={(e) => setRefinePrompt(e.target.value)}
                className="w-full border rounded p-2 mb-2"
                rows="3"
                placeholder="E.g., Make it more concise, add more details, change the tone..."
              />
              <button
                onClick={handleRefine}
                disabled={loading || !refinePrompt.trim()}
                className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 disabled:opacity-50"
              >
                {loading ? 'Refining...' : 'Apply Refinement'}
              </button>
            </div>
          )}

          {showComments && (
            <div className="mt-4 p-4 bg-blue-50 rounded">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Add a comment:
              </label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                className="w-full border rounded p-2 mb-2"
                rows="2"
                placeholder="Your comment..."
              />
              <button
                onClick={handleAddComment}
                disabled={!comment.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
              >
                Add Comment
              </button>
            </div>
          )}
        </>
      )}

      {!section.content && !loading && (
        <p className="text-gray-400 italic">No content generated yet. Click Generate to create content using AI.</p>
      )}
    </div>
  );
}
