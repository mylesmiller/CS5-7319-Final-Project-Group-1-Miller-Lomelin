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
    const dueTime = document.getElementById('taskDueTime').value;
    if (dueDate) {
        // Combine date and time, default to noon if no time is provided
        const dateTimeString = dueTime ? `${dueDate}T${dueTime}` : `${dueDate}T12:00`;
        taskData.due_date = new Date(dateTimeString).toISOString();
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
            // Format date as YYYY-MM-DD
            const dateStr = dueDate.toISOString().slice(0, 10);
            // Format time as HH:MM
            const timeStr = dueDate.toTimeString().slice(0, 5);
            document.getElementById('taskDueDate').value = dateStr;
            document.getElementById('taskDueTime').value = timeStr;
        } else {
            document.getElementById('taskDueDate').value = '';
            document.getElementById('taskDueTime').value = '';
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
    // Load users for the dropdown
    try {
        const usersResponse = await fetch('/api/users');
        const users = await usersResponse.json();
        
        // Populate the assign modal dropdown
        const assignSelect = document.getElementById('assignUserSelect');
        assignSelect.innerHTML = '<option value="">Unassigned</option>';
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user.id;
            option.textContent = `${user.username} (ID: ${user.id})`;
            assignSelect.appendChild(option);
        });
        
        // Get current task to pre-select assigned user
        const taskResponse = await fetch(`/api/tasks/${taskId}`);
        const task = await taskResponse.json();
        if (task.assigned_to) {
            assignSelect.value = task.assigned_to;
        }
        
        // Store task ID for the form submission
        document.getElementById('assignTaskId').value = taskId;
        
        // Show the modal
        document.getElementById('assignModal').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Error loading users');
    }
}

async function saveAssignment() {
    const taskId = document.getElementById('assignTaskId').value;
    const userId = document.getElementById('assignUserSelect').value;
    
    try {
        const response = await fetch(`/api/tasks/${taskId}/assign`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId ? parseInt(userId) : null })
        });
        
        if (response.ok) {
            closeAssignModal();
            location.reload();
        } else {
            const error = await response.json();
            alert(error.error || 'Error assigning task');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error assigning task');
    }
}

function closeAssignModal() {
    document.getElementById('assignModal').style.display = 'none';
}

// User management functions
async function createUser() {
    const username = document.getElementById('userUsername').value;
    const email = document.getElementById('userEmail').value;
    
    if (!username || !email) {
        alert('Please fill in all required fields');
        return;
    }
    
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email })
        });
        
        if (response.ok) {
            closeUserModal();
            location.reload();
        } else {
            const error = await response.json();
            alert(error.error || 'Error creating user');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating user');
    }
}

async function deleteUser(userId, username) {
    if (!confirm(`Are you sure you want to delete ${username}? This action cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/users/${userId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            location.reload();
        } else {
            const error = await response.json();
            alert(error.error || 'Error deleting user');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting user');
    }
}

function showCreateUserModal() {
    document.getElementById('userForm').reset();
    document.getElementById('userModalTitle').textContent = 'Add New Team Member';
    document.getElementById('userModal').style.display = 'block';
}

function closeUserModal() {
    document.getElementById('userModal').style.display = 'none';
}

function showCreateTaskModal() {
    document.getElementById('taskForm').reset();
    document.getElementById('taskId').value = '';
    document.getElementById('taskDueDate').value = '';
    document.getElementById('taskDueTime').value = '';
    document.getElementById('modalTitle').textContent = 'Create Task';
    document.getElementById('taskModal').style.display = 'block';
}

function closeTaskModal() {
    document.getElementById('taskModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const taskModal = document.getElementById('taskModal');
    if (taskModal && event.target == taskModal) {
        taskModal.style.display = 'none';
    }
    
    const assignModal = document.getElementById('assignModal');
    if (assignModal && event.target == assignModal) {
        assignModal.style.display = 'none';
    }
    
    const userModal = document.getElementById('userModal');
    if (userModal && event.target == userModal) {
        userModal.style.display = 'none';
    }
    
    const calendarTaskModal = document.getElementById('calendarTaskModal');
    if (calendarTaskModal && event.target == calendarTaskModal) {
        calendarTaskModal.style.display = 'none';
    }
}

// Calendar state
let calendarState = {
    currentMonth: new Date().getMonth(),
    currentYear: new Date().getFullYear(),
    tasks: []
};

// Calendar rendering
function renderCalendar(tasks, month = null, year = null) {
    const calendar = document.getElementById('calendar');
    if (!calendar) {
        console.error('Calendar element not found');
        return;
    }
    
    // Update state
    if (tasks) calendarState.tasks = tasks;
    if (month !== null) calendarState.currentMonth = month;
    if (year !== null) calendarState.currentYear = year;
    
    const currentMonth = calendarState.currentMonth;
    const currentYear = calendarState.currentYear;
    
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const monthName = new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long', year: 'numeric' });
    
    // Month navigation
    const prevMonth = currentMonth === 0 ? 11 : currentMonth - 1;
    const prevYear = currentMonth === 0 ? currentYear - 1 : currentYear;
    const nextMonth = currentMonth === 11 ? 0 : currentMonth + 1;
    const nextYear = currentMonth === 11 ? currentYear + 1 : currentYear;
    
    let html = '<div class="calendar-header">';
    html += `<button class="calendar-nav-btn" onclick="changeMonth(${prevMonth}, ${prevYear})">&larr; Previous</button>`;
    html += `<h3>${monthName}</h3>`;
    html += `<button class="calendar-nav-btn" onclick="changeMonth(${nextMonth}, ${nextYear})">Next &rarr;</button>`;
    html += '</div>';
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
        
        const dayTasks = calendarState.tasks.filter(task => {
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
        
        // Check if today
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const isToday = date.getTime() === today.getTime();
        
        html += `<div class="calendar-day ${isToday ? 'today' : ''}">`;
        html += `<div class="day-number">${day}</div>`;
        
        if (dayTasks.length > 0) {
            html += '<div class="day-tasks-list">';
            // Show up to 3 tasks, then show "+X more"
            const maxVisible = 3;
            const visibleTasks = dayTasks.slice(0, maxVisible);
            const remaining = dayTasks.length - maxVisible;
            
            visibleTasks.forEach(task => {
                const priorityClass = `priority-${task.priority || 'medium'}`;
                const statusClass = `status-${task.status || 'pending'}`;
                html += `<div class="calendar-task-item ${priorityClass}" onclick="showTaskDetails(${task.id})" title="${task.title}">`;
                html += `<span class="task-title">${task.title}</span>`;
                if (task.assigned_to_username) {
                    html += `<span class="task-assignee-badge">${task.assigned_to_username}</span>`;
                }
                html += `</div>`;
            });
            
            if (remaining > 0) {
                html += `<div class="calendar-task-more" onclick="showDayTasks(${day}, ${currentMonth}, ${currentYear})">+${remaining} more</div>`;
            }
            html += '</div>';
        }
        html += `</div>`;
    }
    
    html += '</div>';
    calendar.innerHTML = html;
}

function changeMonth(month, year) {
    renderCalendar(null, month, year);
}

function showTaskDetails(taskId) {
    const task = calendarState.tasks.find(t => t.id === taskId);
    if (!task) return;
    
    // Populate task details modal
    document.getElementById('calendarTaskId').textContent = task.id;
    document.getElementById('calendarTaskTitle').textContent = task.title;
    document.getElementById('calendarTaskDescription').textContent = task.description || 'No description';
    
    const statusElement = document.getElementById('calendarTaskStatus');
    statusElement.textContent = task.status ? task.status.replace('_', ' ').toUpperCase() : 'PENDING';
    statusElement.className = `status-badge status-${task.status || 'pending'}`;
    
    const priorityElement = document.getElementById('calendarTaskPriority');
    priorityElement.textContent = task.priority ? task.priority.toUpperCase() : 'MEDIUM';
    priorityElement.className = `priority-badge priority-${task.priority || 'medium'}`;
    
    if (task.due_date) {
        const dueDate = new Date(task.due_date);
        document.getElementById('calendarTaskDueDate').textContent = dueDate.toLocaleString('default', { 
            month: 'long', 
            day: 'numeric', 
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit'
        });
    } else {
        document.getElementById('calendarTaskDueDate').textContent = 'No due date';
    }
    
    if (task.assigned_to_username) {
        document.getElementById('calendarTaskAssignee').textContent = task.assigned_to_username;
        document.getElementById('calendarTaskAssigneeRow').style.display = 'block';
    } else {
        document.getElementById('calendarTaskAssigneeRow').style.display = 'none';
    }
    
    // Show modal
    document.getElementById('calendarTaskModal').style.display = 'block';
}

function closeCalendarTaskModal() {
    document.getElementById('calendarTaskModal').style.display = 'none';
}

function showDayTasks(day, month, year) {
    const date = new Date(year, month, day);
    date.setHours(0, 0, 0, 0);
    
    const dayTasks = calendarState.tasks.filter(task => {
        if (!task.due_date) return false;
        try {
            const taskDate = new Date(task.due_date);
            taskDate.setHours(0, 0, 0, 0);
            return taskDate.getTime() === date.getTime();
        } catch (e) {
            return false;
        }
    });
    
    // Show all tasks for that day
    if (dayTasks.length > 0) {
        // Show the first task details
        showTaskDetails(dayTasks[0].id);
    }
}

