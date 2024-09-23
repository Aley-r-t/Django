import {useForm} from 'react-hook-form';
import { createTask } from '../api/tasks.api';
import {useNavigate} from 'react-router-dom';

export function TaskFormPage(){
    const {register,handleSubmit, formState:{
        errors
    }} = useForm();

    const onSubmit = handleSubmit((data)=>{
        console.log(data);
        createTask(data).then((response)=>{
            console.log(response);
        }).catch((error)=>{
            console.log(error);
        })
    });
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
        </div>
    )
}