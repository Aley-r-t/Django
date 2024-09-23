export function TaskCard({ task }){
    return(
        <div key={task.id}>
                <h1>{task.title}</h1>
                <p>{task.description}</p>
                <hr />
        </div>
    )
}