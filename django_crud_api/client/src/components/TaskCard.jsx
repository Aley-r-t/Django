import { useNavigate, useNavigationType } from "react-router-dom"

export function TaskCard({ task }){

    const navigate = useNavigate();
    return(
        <div className="bg-zinc-800 p-3 hover:bg-zinc-700 hover:cursor-pointer" style={{ background: "black" }}
            onClick={()=>{
                navigate(`/tasks/${task.id}`);
               }
            }
        key={task.id}>
                <h1 className="font-bold uppercase">{task.title}</h1>
                <p className="text-slate-400">{task.description}</p>
                <hr />
        </div>
    )
}