import { useEffect, useState } from 'react';
import {getAllTasks} from '../api/tasks.api';

export function TasksList(){
    const [tasks, setTasks] = useState([]);

    useEffect(() => {
        async function loadTasks(){
           const res = await getAllTasks();
        setTasks(res.data);
        }
        loadTasks();
    },[])

    return <div>
        {tasks.map(task => (
            <div key={task.id}>
                <h1>{task.title}</h1>
                <p>{task.description}</p>
            </div>
        ))}   
    </div>
}