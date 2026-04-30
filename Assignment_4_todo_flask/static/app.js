document.addEventListener("DOMContentLoaded", loadTasks);

let currentFilter = 'all';

async function loadTasks(){
    try{
        let url = '/api/tasks';
        if(currentFilter !== 'all'){
            url += '?status=' + currentFilter;
        }

        const res = await fetch(url);
        const data = await res.json();

        const list = document.getElementById('task-list');
        list.innerHTML = "";

        if(data.length === 0){
            document.getElementById('empty').style.display='block';
        } else {
            document.getElementById('empty').style.display='none';
        }

        data.forEach(t=>{
            const div = document.createElement('div');
            div.className = 'task ' + t.priority + (t.completed ? ' completed':'');
            div.innerHTML = `
            <input type="checkbox" ${t.completed ? 'checked':''} onclick="toggleTask(${t.id})">
            <span>${t.title}</span>
            <button onclick="editTask(${t.id}, '${t.title}')">Edit</button>
            <button onclick="deleteTask(${t.id})">Delete</button>
            `;
            list.appendChild(div);
        });

        updateCounter(data);

    }catch(e){
        alert("Error loading tasks");
    }
}

async function addTask(){
    const title = document.getElementById('title').value;
    if(!title){
        alert("Title required");
        return;
    }

    await fetch('/api/tasks',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({title})
    });

    document.getElementById('title').value="";
    loadTasks();
}

async function deleteTask(id){
    await fetch('/api/tasks/'+id,{method:'DELETE'});
    loadTasks();
}

async function toggleTask(id){
    await fetch('/api/tasks/'+id+'/toggle',{method:'PATCH'});
    loadTasks();
}

async function editTask(id, oldTitle){
    const newTitle = prompt("Edit task:", oldTitle);
    if(!newTitle) return;

    await fetch('/api/tasks/'+id,{
        method:'PUT',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({title:newTitle})
    });

    loadTasks();
}

function filterTasks(status){
    currentFilter = status;
    loadTasks();
}

function updateCounter(tasks){
    let total = tasks.length;
    let completed = tasks.filter(t=>t.completed).length;
    let active = total - completed;

    document.getElementById('counter').innerText =
    `Total:${total} Active:${active} Completed:${completed}`;
}
