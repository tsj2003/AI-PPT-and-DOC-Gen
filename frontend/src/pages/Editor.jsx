import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Download, ArrowLeft, Sparkles, HelpCircle } from 'lucide-react';
import { getProject } from '../api/projects';
import { exportProject } from '../api/llm';
import Navbar from '../components/Navbar';
import SectionCard from '../components/SectionCard';

export default function Editor() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [includeImages, setIncludeImages] = useState(false);

  useEffect(() => {
    loadProject();
  }, [projectId]);

  const loadProject = async () => {
    try {
      const data = await getProject(projectId);
      setProject(data);
    } catch (error) {
      alert('Failed to load project: ' + error.message);
      navigate('/dashboard');
    }
    setLoading(false);
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const response = await exportProject(projectId, includeImages);
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const extension = project.document_type === 'docx' ? '.docx' : '.pptx';
      link.setAttribute('download', `${project.title}${extension}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert('Failed to export project: ' + error.message);
    }
    setExporting(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100">
        <Navbar />
        <div className="flex items-center justify-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="h-6 w-6" />
            </button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{project.title}</h1>
              <p className="text-gray-600 mt-1">{project.topic}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            {project.document_type === 'pptx' && (
              <div className="flex items-center space-x-2 bg-gradient-to-r from-purple-50 to-pink-50 px-4 py-2 rounded-md border-2 border-purple-200">
                <input
                  type="checkbox"
                  checked={includeImages}
                  onChange={(e) => setIncludeImages(e.target.checked)}
                  className="w-5 h-5 rounded cursor-pointer"
                  id="generate-images-checkbox"
                />
                <label htmlFor="generate-images-checkbox" className="flex items-center space-x-2 cursor-pointer">
                  <Sparkles className="h-4 w-4 text-purple-600" />
                  <span className="font-semibold text-purple-700">AI Generate Images</span>
                </label>
                <div className="group relative">
                  <HelpCircle className="h-4 w-4 text-purple-400 cursor-help" />
                  <div className="invisible group-hover:visible absolute right-0 z-10 w-48 p-3 bg-gray-800 text-white text-xs rounded-md shadow-lg bottom-full mb-2">
                    ✨ AI will create professional images for each slide based on the slide title and your project topic. Takes ~30 seconds.
                  </div>
                </div>
              </div>
            )}
            <button
              onClick={handleExport}
              disabled={exporting}
              className="flex items-center space-x-2 bg-green-600 text-white px-5 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-all"
            >
              <Download className="h-5 w-5" />
              <span>{exporting ? 'Exporting...' : 'Export'}</span>
            </button>
          </div>
        </div>

        <div className="mb-4">
          <span className={`inline-block px-3 py-1 text-sm font-medium rounded ${
            project.document_type === 'docx' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
          }`}>
            {project.document_type === 'docx' ? 'Word Document' : 'PowerPoint Presentation'}
          </span>
        </div>

        <div className="space-y-4">
          {project.sections && project.sections.length > 0 ? (
            project.sections
              .sort((a, b) => a.order - b.order)
              .map((section) => (
                <SectionCard 
                  key={section.id} 
                  section={section} 
                  onUpdate={loadProject}
                  projectType={project.document_type}
                  projectTopic={project.topic}
                />
              ))
          ) : (
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <p className="text-gray-600">No sections found in this project.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
