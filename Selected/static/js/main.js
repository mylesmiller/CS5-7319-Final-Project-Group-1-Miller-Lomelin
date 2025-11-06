// Main JavaScript for task management

// Task CRUD operations
async function saveTask() {
    const taskId = document.getElementById('taskId').value;
    const taskData = {
        title: document.getElementById('taskTitle').value,
        description: document.getElementById('taskDescription').value,
        priority: document.getElementById('taskPriority').value,
        status: document.getElementById('taskStatus').value,
        assigned_to: document.getElementById('taskAssignee').value || null
    };
    
    const dueDate = document.getElementById('taskDueDate').value;
    if (dueDate) {
        taskData.due_date = new Date(dueDate).toISOString();
    }
    
    try {
        const url = taskId ? `/api/tasks/${taskId}` : '/api/tasks';
        const method = taskId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Error saving task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error saving task');
    }
}

async function editTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const task = await response.json();
        
        document.getElementById('taskId').value = task.id;
        document.getElementById('taskTitle').value = task.title;
        document.getElementById('taskDescription').value = task.description || '';
        document.getElementById('taskPriority').value = task.priority;
        document.getElementById('taskStatus').value = task.status;
        document.getElementById('taskAssignee').value = task.assigned_to || '';
        
        if (task.due_date) {
            const dueDate = new Date(task.due_date);
            document.getElementById('taskDueDate').value = dueDate.toISOString().slice(0, 16);
        }
        
        document.getElementById('modalTitle').textContent = 'Edit Task';
        document.getElementById('taskModal').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Error loading task');
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Error deleting task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting task');
    }
}

async function assignTask(taskId) {
    const userId = prompt('Enter user ID to assign:');
    if (!userId) return;
    
    try {
        const response = await fetch(`/api/tasks/${taskId}/assign`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: parseInt(userId) })
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Error assigning task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error assigning task');
    }
}

function showCreateTaskModal() {
    document.getElementById('taskForm').reset();
    document.getElementById('taskId').value = '';
    document.getElementById('modalTitle').textContent = 'Create Task';
    document.getElementById('taskModal').style.display = 'block';
}

function closeTaskModal() {
    document.getElementById('taskModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('taskModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Calendar rendering
function renderCalendar(tasks) {
    const calendar = document.getElementById('calendar');
    if (!calendar) {
        console.error('Calendar element not found');
        return;
    }
    
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    
    let html = '<h3>' + now.toLocaleString('default', { month: 'long', year: 'numeric' }) + '</h3>';
    html += '<div class="calendar-grid">';
    
    // Day headers
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    days.forEach(day => {
        html += `<div class="calendar-day-header">${day}</div>`;
    });
    
    // Empty cells for days before month starts
    for (let i = 0; i < firstDay.getDay(); i++) {
        html += '<div class="calendar-day empty"></div>';
    }
    
    // Days of the month
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const date = new Date(currentYear, currentMonth, day);
        // Normalize date to midnight for comparison
        date.setHours(0, 0, 0, 0);
        
        const dayTasks = tasks.filter(task => {
            if (!task.due_date) return false;
            try {
                const taskDate = new Date(task.due_date);
                taskDate.setHours(0, 0, 0, 0);
                return taskDate.getTime() === date.getTime();
            } catch (e) {
                console.error('Error parsing task date:', task.due_date, e);
                return false;
            }
        });
        
        html += `<div class="calendar-day">`;
        html += `<div class="day-number">${day}</div>`;
        if (dayTasks.length > 0) {
            html += `<div class="day-tasks">${dayTasks.length} task(s)</div>`;
            // Add task titles on hover
            const taskTitles = dayTasks.map(t => t.title).join(', ');
            html += `<div class="day-tasks-detail" style="display:none;">${taskTitles}</div>`;
        }
        html += `</div>`;
    }
    
    html += '</div>';
    calendar.innerHTML = html;
}

