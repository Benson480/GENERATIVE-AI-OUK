# main.jac - entrypoint
import walkers

# Expose simple http walker that the Jac server can call (example)
walker http_api(string repo_url):
    # create a session node to hold results
    create node:session {
        props.url = repo_url
        props.status = "started"
    } -> ses

    # delegate to supervisor walker
    walkers.supervisor(ses)
    return ses.props
