import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Trash2, FileText, Presentation, Sparkles } from 'lucide-react';
import { createProject } from '../api/projects';
import { generateTitle, generateOutline } from '../api/ai';
import Navbar from '../components/Navbar';

export default function CreateProject() {
  const [title, setTitle] = useState('');
  const [topic, setTopic] = useState('');
  const [documentType, setDocumentType] = useState('docx');
  const [sections, setSections] = useState([{ title: '', order: 0 }]);
  const [loading, setLoading] = useState(false);
  const [generatingTitle, setGeneratingTitle] = useState(false);
  const [generatingOutline, setGeneratingOutline] = useState(false);
  const navigate = useNavigate();

  const addSection = () => {
    setSections([...sections, { title: '', order: sections.length }]);
  };

  const removeSection = (index) => {
    if (sections.length === 1) return;
    setSections(sections.filter((_, i) => i !== index).map((s, i) => ({ ...s, order: i })));
  };

  const updateSectionTitle = (index, value) => {
    const updated = [...sections];
    updated[index].title = value;
    setSections(updated);
  };

  const handleGenerateTitle = async () => {
    if (!topic.trim()) {
      alert('Please enter a topic first');
      return;
    }
    setGeneratingTitle(true);
    try {
      const generatedTitle = await generateTitle(topic);
      setTitle(generatedTitle);
    } catch (error) {
      alert('Failed to generate title: ' + error.message);
    }
    setGeneratingTitle(false);
  };

  const handleGenerateOutline = async () => {
    if (!topic.trim()) {
      alert('Please enter a topic first');
      return;
    }
    setGeneratingOutline(true);
    try {
      const outline = await generateOutline(topic, documentType, 5);
      setSections(outline);
    } catch (error) {
      alert('Failed to generate outline: ' + error.message);
    }
    setGeneratingOutline(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (sections.some(s => !s.title.trim())) {
      alert('Please fill in all section titles');
      return;
    }

    setLoading(true);
    try {
      const projectData = {
        title,
        topic,
        document_type: documentType,
        sections: sections.map((s, i) => ({ title: s.title, order: i }))
      };
      
      const project = await createProject(projectData);
      navigate(`/editor/${project.id}`);
    } catch (error) {
      alert('Failed to create project: ' + error.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Create New Project</h1>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Title
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                  placeholder="e.g., Marketing Plan 2024"
                />
                <button
                  type="button"
                  onClick={handleGenerateTitle}
                  disabled={generatingTitle || !topic}
                  className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Sparkles className="h-4 w-4" />
                  {generatingTitle ? 'Generating...' : 'AI Title'}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Topic
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                placeholder="e.g., Digital Marketing Strategy for E-commerce"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Document Type
              </label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => setDocumentType('docx')}
                  className={`flex items-center justify-center space-x-2 p-4 border-2 rounded-lg ${
                    documentType === 'docx' ? 'border-blue-600 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <FileText className="h-8 w-8 text-blue-600" />
                  <span className="font-medium">Word Document</span>
                </button>
                <button
                  type="button"
                  onClick={() => setDocumentType('pptx')}
                  className={`flex items-center justify-center space-x-2 p-4 border-2 rounded-lg ${
                    documentType === 'pptx' ? 'border-green-600 bg-green-50' : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <Presentation className="h-8 w-8 text-green-600" />
                  <span className="font-medium">PowerPoint</span>
                </button>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-4">
                <label className="block text-sm font-medium text-gray-700">
                  {documentType === 'docx' ? 'Sections' : 'Slides'}
                </label>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={handleGenerateOutline}
                    disabled={generatingOutline || !topic}
                    className="flex items-center gap-1 px-3 py-1 bg-purple-600 text-white text-sm rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Sparkles className="h-4 w-4" />
                    {generatingOutline ? 'Generating...' : 'AI Outline'}
                  </button>
                  <button
                    type="button"
                    onClick={addSection}
                    className="flex items-center space-x-1 text-blue-600 hover:text-blue-700"
                  >
                    <Plus className="h-4 w-4" />
                    <span>Add {documentType === 'docx' ? 'Section' : 'Slide'}</span>
                  </button>
                </div>
              </div>

              <div className="space-y-3">
                {sections.map((section, index) => (
                  <div key={index} className="flex space-x-2">
                    <input
                      type="text"
                      value={section.title}
                      onChange={(e) => updateSectionTitle(index, e.target.value)}
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder={`${documentType === 'docx' ? 'Section' : 'Slide'} ${index + 1} title`}
                      required
                    />
                    {sections.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeSection(index)}
                        className="px-3 py-2 bg-red-100 text-red-600 rounded-md hover:bg-red-200"
                      >
                        <Trash2 className="h-5 w-5" />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="flex space-x-4 pt-6">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Project'}
              </button>
              <button
                type="button"
                onClick={() => navigate('/dashboard')}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
