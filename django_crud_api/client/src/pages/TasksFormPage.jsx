import { useEffect } from 'react';
import {set, useForm} from 'react-hook-form';
import { createTask, deleteTasks, updateTasks,getTask } from '../api/tasks.api';
import {Navigate, useNavigate,useParams } from 'react-router-dom';

export function TaskFormPage(){
    const {register,handleSubmit, 
        formState:{errors},
        setValue
    } = useForm();
    
    const params  = useParams();
   

    const onSubmit = handleSubmit(async (data)=>{
        if(params.id){
            updateTasks(params.id,data);
        } else {
            await createTask(data);
        }
        Navigate("/tasks");
    });

    useEffect(()=>{
        async function loadTask(){
            if (params.id){
               const {data:{title, description}} =  await getTask(params.id)
               setValue ('title',title);
                setValue('description',description);
            }
        }
        loadTask();

    },[]);

    return(
        <div>
            <form onSubmit={onSubmit}>
                <input type="text" 
                placeholder="Title" 
                {...register("title",{required:true})}
                />
                {errors.title && <span>Title is required</span>}
                <textarea
                
                 placeholder="Description"
                {...register("description",{required:true})}
                ></textarea>
                {errors.description && <span>Description is required</span>}
                <button type="submit">Create Task</button>
            </form>

            { params.id && <button onClick={async () =>{
                const accepted = window.confirm("Are you sure you want to delete this task?")
                if(accepted){
                    await deleteTasks(params.id).then((response)=>{
                        console.log(response);
                    }).catch((error)=>{
                        console.log(error);
                    })
                }
            }}>Delete</button>}
        </div>
    )
}