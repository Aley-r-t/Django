import {Link} from 'react-router-dom';

export function Navigation(){
    return(
        <div>
            <Link to="/tasks">Task App</Link><br/>
            <Link to="/tasks-create">Create Task</Link>
        </div>
    )
}

