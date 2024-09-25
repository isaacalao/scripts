#######################################
# Print error message to standard output.
# Globals:
# 	None
# Arguments:
# 	Ok status message
# Outputs:
# 	Message
######################################
function lib::ok() {
  printf "\x1B[32m%s\x1B[0m\n" "$1" >&1
}

#######################################
# Print error message to standard error.
# Globals:
# 	None
# Arguments:
# 	Err status message
# Outputs:
# 	Message
######################################
function lib::err() {
  printf "\x1B[31m%s\x1B[0m\n" "$1" >&2 
}

#######################################
# Map corresponding key to numerical index.
# Globals:
# 	None
# Arguments:
# 	Key
# Outputs:
# 	Index for hashmap
######################################
function lib::hashmap_func() {
  case $1 in
    ("}") printf 0;;
    ("]") printf 1;;
    (")") printf 2;;
    ("{" | "[" | "(") printf 3;;
    (*) printf 4;;
  esac
}

# TODO(isaacalao)
#######################################
# Dummy pipeline!
# Globals:
# 	None
# Arguments:
# 	None
# Outputs:
# 	Dummy output
######################################
function lib::dummy_pipeline() {
  printf "MAC IP TCP DATA\n" \
    | awk '{ print $0}' \
    | awk '{ print $2" "$3" "$4}' \
    | awk '{ print $2" "$3 }' \
    | awk '{ print $2 }'
}
