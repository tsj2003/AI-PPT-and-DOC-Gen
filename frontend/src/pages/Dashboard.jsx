import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plus, FileText, Trash2, Edit } from 'lucide-react';
import { getProjects, deleteProject } from '../api/projects';
import Navbar from '../components/Navbar';

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (error) {
      alert('Failed to load projects: ' + error.message);
    }
    setLoading(false);
  };

  const handleDelete = async (projectId) => {
    if (!confirm('Are you sure you want to delete this project?')) return;

    try {
      await deleteProject(projectId);
      loadProjects();
    } catch (error) {
      alert('Failed to delete project: ' + error.message);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Projects</h1>
          <Link
            to="/create"
            className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            <Plus className="h-5 w-5" />
            <span>New Project</span>
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading projects...</p>
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <FileText className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">No projects yet</h3>
            <p className="text-gray-600 mb-6">Get started by creating your first document or presentation!</p>
            <Link
              to="/create"
              className="inline-flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
            >
              <Plus className="h-5 w-5" />
              <span>Create Your First Project</span>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <div key={project.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{project.title}</h3>
                      <p className="text-sm text-gray-600">{project.topic}</p>
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded ${
                      project.document_type === 'docx' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                    }`}>
                      {project.document_type.toUpperCase()}
                    </span>
                  </div>

                  <div className="text-sm text-gray-500 mb-4">
                    <p>Created: {formatDate(project.created_at)}</p>
                    <p>Sections: {project.sections?.length || 0}</p>
                  </div>

                  <div className="flex space-x-2">
                    <Link
                      to={`/editor/${project.id}`}
                      className="flex-1 flex items-center justify-center space-x-1 bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700"
                    >
                      <Edit className="h-4 w-4" />
                      <span>Edit</span>
                    </Link>
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="flex items-center justify-center bg-red-600 text-white px-3 py-2 rounded hover:bg-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
