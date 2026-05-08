// Smart Task Manager - Core JS
const socket = io();

// State
let tasks = [];
let stats = {};

// Helpers
const showToast = (msg, type = 'primary') => {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-dark border-primary show position-fixed bottom-0 end-0 m-3`;
    toast.innerHTML = `<div class="d-flex"><div class="toast-body text-white">${msg}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
};

// WebSocket Events
socket.on('task_added', (task) => {
    showToast(`New Task: ${task.title}`);
    refreshData();
});

socket.on('task_updated', (task) => {
    showToast(`Updated: ${task.title}`);
    refreshData();
});

socket.on('task_deleted', () => {
    showToast(`Task Deleted`, 'danger');
    refreshData();
});

socket.on('task_completed', (task) => {
    showToast(`Task Completed! 🎉`, 'success');
    confettiAnimation();
});

// API Calls
async function refreshData() {
    await fetchTasks();
    await fetchStats();
}

async function fetchTasks() {
    try {
        const res = await fetch('/api/tasks');
        tasks = await res.json();
        renderTasks();
    } catch (e) { console.error(e); }
}

async function fetchStats() {
    try {
        const res = await fetch('/api/analytics');
        stats = await res.json();
        renderStats();
    } catch (e) { console.error(e); }
}

// Rendering
function renderTasks() {
    const container = document.getElementById('taskContainer');
    if (!container) return;

    const searchTerm = document.getElementById('searchTask')?.value.toLowerCase() || '';
    const priorityFilter = document.getElementById('filterPriority')?.value || 'All';

    const filtered = tasks.filter(t => {
        const matchesSearch = t.title.toLowerCase().includes(searchTerm);
        const matchesPriority = priorityFilter === 'All' || t.priority === priorityFilter;
        return matchesSearch && matchesPriority;
    });

    if (filtered.length === 0) {
        container.innerHTML = `<div class="text-center py-5 text-muted">No tasks found.</div>`;
        return;
    }

    container.innerHTML = `
        <table class="custom-table">
            <thead>
                <tr class="text-muted small uppercase">
                    <td>Title</td>
                    <td>Priority</td>
                    <td>Status</td>
                    <td>Due Date</td>
                    <td class="text-end">Actions</td>
                </tr>
            </thead>
            <tbody>
                ${filtered.map(t => `
                    <tr class="animate-fade">
                        <td>
                            <div class="fw-bold">${t.title}</div>
                            <div class="small text-muted">${t.description || ''}</div>
                        </td>
                        <td><span class="badge bg-${t.priority === 'High' ? 'danger' : t.priority === 'Medium' ? 'warning' : 'success'}">${t.priority}</span></td>
                        <td>
                            <span class="badge bg-${t.status === 'Completed' ? 'primary' : (t.is_overdue ? 'danger' : 'secondary')}">
                                ${t.status === 'Completed' ? 'Completed' : (t.is_overdue ? 'Overdue' : 'Pending')}
                            </span>
                        </td>
                        <td><small>${t.due_date ? new Date(t.due_date).toLocaleDateString() : '-'}</small></td>
                        <td class="text-end">
                            <button class="btn btn-sm text-primary" onclick="openEditModal(${t.id})"><i class="bi bi-pencil"></i></button>
                            <button class="btn btn-sm text-danger" onclick="deleteTask(${t.id})"><i class="bi bi-trash"></i></button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function renderStats() {
    if (document.getElementById('totalTasks')) {
        document.getElementById('totalTasks').innerText = stats.total_tasks;
        document.getElementById('completedTasks').innerText = stats.completed_tasks;
        document.getElementById('pendingTasks').innerText = stats.pending_tasks;
        document.getElementById('completionPct').innerText = `${stats.completion_percentage}%`;
        
        const progressBar = document.getElementById('completionBar');
        if (progressBar) {
            progressBar.style.width = `${stats.completion_percentage}%`;
        }
    }
}

// Actions
async function deleteTask(id) {
    if (confirm('Delete this task?')) {
        await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
        refreshData();
    }
}

async function openEditModal(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    document.getElementById('editTaskId').value = task.id;
    document.getElementById('editTaskTitle').value = task.title;
    document.getElementById('editTaskDesc').value = task.description || '';
    document.getElementById('editTaskPriority').value = task.priority;
    document.getElementById('editTaskStatus').value = task.status;
    if (task.due_date) {
        document.getElementById('editTaskDueDate').value = task.due_date.split('T')[0];
    }

    const modal = new bootstrap.Modal(document.getElementById('editTaskModal'));
    modal.show();
}

// Dark Mode
function toggleDarkMode() {
    document.body.classList.toggle('light-mode');
    const isLight = document.body.classList.contains('light-mode');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'light') document.body.classList.add('light-mode');
    refreshData();

    // Form Submissions
    document.getElementById('addTaskForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!e.target.checkValidity()) {
            e.stopPropagation();
            e.target.classList.add('was-validated');
            return;
        }

        const data = {
            title: document.getElementById('taskTitle').value,
            description: document.getElementById('taskDesc').value,
            priority: document.getElementById('taskPriority').value,
            due_date: document.getElementById('taskDueDate').value
        };
        const res = await fetch('/api/tasks', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById('addTaskModal')).hide();
            e.target.reset();
            e.target.classList.remove('was-validated');
            refreshData();
        }
    });

    document.getElementById('editTaskForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!e.target.checkValidity()) {
            e.stopPropagation();
            e.target.classList.add('was-validated');
            return;
        }

        const id = document.getElementById('editTaskId').value;
        const data = {
            title: document.getElementById('editTaskTitle').value,
            description: document.getElementById('editTaskDesc').value,
            priority: document.getElementById('editTaskPriority').value,
            status: document.getElementById('editTaskStatus').value,
            due_date: document.getElementById('editTaskDueDate').value
        };

        const res = await fetch(`/api/tasks/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById('editTaskModal')).hide();
            refreshData();
        }
    });
});

function confettiAnimation() {
    // Basic placeholder for confetti logic
    console.log("CONFETTI!");
}
