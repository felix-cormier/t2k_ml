myfunction() {
    #do things with parameters like $1 such as
    python3 -m debugpy --listen nc20237:1080 --wait-for-client $@
}


myfunction $@ #calls `myfunction`
