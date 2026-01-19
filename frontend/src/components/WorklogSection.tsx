import { useState, useEffect } from 'react';
import { Clock, Plus, Edit2, Trash2, Loader2, AlertCircle, Save } from 'lucide-react';
import type { Worklog, CreateWorklogRequest, UpdateWorklogRequest } from '../types/worklog';
import { getCardWorklogs, createWorklog, updateWorklog, deleteWorklog } from '../api/worklogs';

interface WorklogSectionProps {
  cardId: number;
}

interface WorklogFormErrors {
  date?: string;
  hours?: string;
  note?: string;
}

const WorklogSection = ({ cardId }: WorklogSectionProps) => {
  const [worklogs, setWorklogs] = useState<Worklog[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  // Form state
  const [date, setDate] = useState('');
  const [hours, setHours] = useState('');
  const [note, setNote] = useState('');
  const [formErrors, setFormErrors] = useState<WorklogFormErrors>({});
  const [apiError, setApiError] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (cardId) {
      loadWorklogs();
    }
  }, [cardId]);

  const loadWorklogs = async () => {
    setIsLoading(true);
    try {
      const data = await getCardWorklogs(cardId);
      setWorklogs(data);
    } catch (err: any) {
      console.error('Error loading worklogs:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setDate('');
    setHours('');
    setNote('');
    setFormErrors({});
    setApiError('');
    setShowForm(false);
    setEditingId(null);
  };

  const validateForm = (): boolean => {
    const errors: WorklogFormErrors = {};

    if (!date) {
      errors.date = 'La fecha es requerida';
    } else {
      const selectedDate = new Date(date);
      const today = new Date();
      today.setHours(23, 59, 59, 999);
      if (selectedDate > today) {
        errors.date = 'La fecha no puede ser futura';
      }
    }

    const hoursNum = parseFloat(hours);
    if (!hours || isNaN(hoursNum)) {
      errors.hours = 'Las horas son requeridas';
    } else if (hoursNum <= 0) {
      errors.hours = 'Las horas deben ser mayores a 0';
    } else if (hoursNum < 0.25) {
      errors.hours = 'El mínimo recomendado es 0.25 horas';
    }

    if (note && note.length > 200) {
      errors.note = 'La nota no puede exceder 200 caracteres';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleCreate = async () => {
    setApiError('');
    if (!validateForm()) return;

    setIsSaving(true);
    try {
      const data: CreateWorklogRequest = {
        date,
        hours: parseFloat(hours),
        note: note.trim() || undefined,
      };
      await createWorklog(cardId, data);
      await loadWorklogs();
      resetForm();
    } catch (err: any) {
      setApiError(err.message || 'Error al crear el registro');
    } finally {
      setIsSaving(false);
    }
  };

  const handleEdit = (worklog: Worklog) => {
    setEditingId(worklog.id);
    setHours(worklog.hours.toString());
    setNote(worklog.note || '');
    setShowForm(true);
    // No permitimos editar la fecha
    setDate(worklog.date);
  };

  const handleUpdate = async () => {
    setApiError('');
    if (!validateForm()) return;

    setIsSaving(true);
    try {
      const data: UpdateWorklogRequest = {
        hours: parseFloat(hours),
        note: note.trim() || undefined,
      };
      await updateWorklog(editingId!, data);
      await loadWorklogs();
      resetForm();
    } catch (err: any) {
      setApiError(err.message || 'Error al actualizar el registro');
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('¿Eliminar este registro de horas?')) return;

    try {
      await deleteWorklog(id);
      await loadWorklogs();
    } catch (err: any) {
      setApiError(err.message || 'Error al eliminar el registro');
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  const totalHours = worklogs.reduce((sum, w) => sum + w.hours, 0);

  return (
    <div className="border-t pt-4">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-semibold text-gray-900 flex items-center gap-2">
          <Clock className="w-4 h-4 text-indigo-600" />
          Horas trabajadas
          {totalHours > 0 && (
            <span className="text-sm font-normal text-gray-500">
              ({totalHours.toFixed(2)}h total)
            </span>
          )}
        </h4>
        {!showForm && (
          <button
            onClick={() => {
              resetForm();
              setShowForm(true);
              setDate(new Date().toISOString().split('T')[0]);
            }}
            className="text-sm text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
          >
            <Plus className="w-4 h-4" />
            Registrar horas
          </button>
        )}
      </div>

      {apiError && (
        <div className="mb-3 p-2 bg-red-50 border border-red-200 rounded text-red-600 text-sm flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {apiError}
        </div>
      )}

      {/* Formulario */}
      {showForm && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
          <h5 className="text-sm font-medium text-gray-700 mb-2">
            {editingId ? 'Editar registro' : 'Nuevo registro'}
          </h5>

          <div className="space-y-2">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Fecha <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                disabled={!!editingId}
                className={`w-full px-2 py-1.5 text-sm border rounded outline-none transition ${
                  formErrors.date
                    ? 'border-red-300 focus:ring-2 focus:ring-red-200'
                    : 'border-gray-300 focus:ring-2 focus:ring-indigo-200'
                } ${editingId ? 'bg-gray-100 cursor-not-allowed' : ''}`}
              />
              {formErrors.date && (
                <span className="text-xs text-red-500 mt-0.5">{formErrors.date}</span>
              )}
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Horas <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                step="0.25"
                min="0.25"
                value={hours}
                onChange={(e) => setHours(e.target.value)}
                className={`w-full px-2 py-1.5 text-sm border rounded outline-none transition ${
                  formErrors.hours
                    ? 'border-red-300 focus:ring-2 focus:ring-red-200'
                    : 'border-gray-300 focus:ring-2 focus:ring-indigo-200'
                }`}
                placeholder="Ej: 2.5"
              />
              {formErrors.hours && (
                <span className="text-xs text-red-500 mt-0.5">{formErrors.hours}</span>
              )}
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">
                Nota (opcional)
              </label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                className={`w-full px-2 py-1.5 text-sm border rounded outline-none transition resize-none ${
                  formErrors.note
                    ? 'border-red-300 focus:ring-2 focus:ring-red-200'
                    : 'border-gray-300 focus:ring-2 focus:ring-indigo-200'
                }`}
                placeholder="Descripción del trabajo realizado..."
                rows={2}
                maxLength={200}
              />
              <div className="flex justify-between mt-0.5">
                {formErrors.note && (
                  <span className="text-xs text-red-500">{formErrors.note}</span>
                )}
                <span className="text-xs text-gray-400 ml-auto">{note.length}/200</span>
              </div>
            </div>
          </div>

          <div className="flex gap-2 mt-3">
            <button
              onClick={editingId ? handleUpdate : handleCreate}
              disabled={isSaving}
              className="flex-1 bg-indigo-600 text-white px-3 py-1.5 rounded text-sm hover:bg-indigo-700 transition disabled:opacity-50 flex items-center justify-center gap-1"
            >
              {isSaving ? (
                <>
                  <Loader2 className="w-3 h-3 animate-spin" />
                  Guardando...
                </>
              ) : (
                <>
                  <Save className="w-3 h-3" />
                  {editingId ? 'Guardar cambios' : 'Crear registro'}
                </>
              )}
            </button>
            <button
              onClick={resetForm}
              disabled={isSaving}
              className="px-3 py-1.5 text-sm text-gray-600 hover:text-gray-800 transition"
            >
              Cancelar
            </button>
          </div>
        </div>
      )}

      {/* Lista de worklogs */}
      <div className="space-y-2 max-h-60 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
          </div>
        ) : worklogs.length === 0 ? (
          <div className="text-center py-8 text-gray-500 text-sm">
            No hay horas registradas para esta tarjeta
          </div>
        ) : (
          worklogs.map((worklog) => (
            <div
              key={worklog.id}
              className="p-2 bg-gray-50 rounded border border-gray-200 hover:border-gray-300 transition group"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 text-sm">
                    <span className="font-medium text-gray-900">
                      {worklog.hours}h
                    </span>
                    <span className="text-gray-500">•</span>
                    <span className="text-gray-600 text-xs">
                      {formatDate(worklog.date)}
                    </span>
                  </div>
                  {worklog.note && (
                    <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                      {worklog.note}
                    </p>
                  )}
                </div>
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition">
                  <button
                    onClick={() => handleEdit(worklog)}
                    className="p-1 text-gray-500 hover:text-indigo-600 transition"
                    title="Editar"
                  >
                    <Edit2 className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={() => handleDelete(worklog.id)}
                    className="p-1 text-gray-500 hover:text-red-600 transition"
                    title="Eliminar"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default WorklogSection;
