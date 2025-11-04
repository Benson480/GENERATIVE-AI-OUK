# walkers.jac - Supervisor, RepoMapper, Analyzer, DocGenie
# This file uses py_module to call Python helpers for heavy IO & parsing

# Supervisor orchestrates everything
walker supervisor(node ses_node):
    # get URL
    local url = ses_node.props.url
    if (!url) {
        ses_node.props.status = "error: no url"
        return
    }
    ses_node.props.status = "cloning"
    # call python to clone repo
    local res = py_module.run("py_helpers.clone_repo.clone_repository", url)
    if (res["ok"] == false) {
        ses_node.props.status = "error: clone failed"
        ses_node.props.error = res["error"]
        return
    }
    ses_node.props.repo_path = res["path"]
    ses_node.props.repo_name = res["name"]

    # produce file tree and README summary
    ses_node.props.status = "mapping"
    local map_res = py_module.run("py_helpers.tree_parser.build_file_tree", res["path"])
    ses_node.props.filetree = map_res["filetree"]
    ses_node.props.top_files = map_res["top_files"]

    local readme_res = py_module.run("py_helpers.readme_summariser.summarise_readme", res["path"])
    ses_node.props.readme_summary = readme_res["summary"]

    # priorities: top files first
    ses_node.props.status = "analyzing"
    for local f in ses_node.props.top_files {
        py_module.run("py_helpers.tree_parser.parse_and_build_ccg", res["path"], f)
    }

    # build full CCG (can be incremental; python stores results under outputs)
    local ccg_res = py_module.run("py_helpers.tree_parser.export_ccg", res["path"])
    ses_node.props.ccg = ccg_res["ccg_summary"]

    ses_node.props.status = "generating_docs"
    local doc_res = py_module.run("py_helpers.docgen.generate_markdown", res["path"], ses_node.props.repo_name)
    ses_node.props.docs_path = doc_res["docs_path"]
    ses_node.props.diagram = doc_res["diagram_path"]
    ses_node.props.status = "done"
    return
