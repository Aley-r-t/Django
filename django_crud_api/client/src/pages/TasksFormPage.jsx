import { useEffect } from 'react';
import {set, useForm} from 'react-hook-form';
import { createTask, deleteTasks, updateTasks,getTask } from '../api/tasks.api';
import {Navigate, useNavigate,useParams } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';

export function TaskFormPage(){
    const {register,handleSubmit, 
        formState:{errors},
        setValue
    } = useForm();
    
    const params  = useParams();
   

    const onSubmit = handleSubmit(async (data)=>{
        if(params.id){
            updateTasks(params.id,data);
            toast.success("Task updated successfully");
        } else {
            await createTask(data);
            toast.success("Task created successfully");
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
        <div className='mx-w-xl mx-auto'>
            <form onSubmit={onSubmit}>
                <input type="text" 
                placeholder="Title" 
                {...register("title",{required:true})}
                className='bg-zinc-700 p-3 rounded-lg block w-full mb-3'
                />
                {errors.title && <span>Title is required</span>}
                <textarea
                
                 placeholder="Description"
                {...register("description",{required:true})}
                className='bg-zinc-700 p-3 rounded-lg block w-full mb-3'
                ></textarea>
                {errors.description && <span>Description is required</span>}
                <button 
                className='bg-indigo-500 p-3 rounded-lg block w-full mt-3'
                type="submit">Create Task</button>
            </form>

            { params.id && <button
            className='bg-red-500 p-3 rounded-lg block w-48 mt-3'
            onClick={async () =>{
                const accepted = window.confirm("Are you sure you want to delete this task?")
                if(accepted){
                    await deleteTasks(params.id).then((response)=>{
                        toast.success("Task deleted successfully");
                    }).catch((error)=>{
                        console.log(error);
                    })
                }
            }}>Delete</button>}
        </div>
    )
}