from os import system

class BashEnumController:
  enum = []

  def __init__(enum):
    self.enum = enum

  def set_enum_from_reference(ref):
    __init__(ref)

  def get_enum_from_reference(ref):
    if ref is None:
      sys.exit(1)

    expression = '"${' + ref + '[@]}"'
    enum = "$( python -c 'import sys; from pyscript import {}; print {}(sys.argv[1:])' {} )".format(BashClass.set_enum_from_reference.__name__, BashClass.set_enum_from_reference.__name__, expression)
    set_enum = "mapfile -t {} <<<\"${}\"".format(ref, enum.__name__)

    try:
      subprocess.run(enum)
    except:
      exception_message = "Exception: Failed to get enumeration."
      print(exception_message)
      __init__()
      sys.exit(1)

    try:
      subprocess.run(set_enum)
    except:
      exception_message = "Exception: Failed to set enumeration."
      print(exception_message)
      __init__()
      sys.exit(1)

class BashVarController:
  var = ""

  def __init__(var):
    self.var = var

  def set_var_from_reference(ref):
    __init__(ref)

  def get_var_from_reference(ref):
    if ref is None:
      sys.exit(1)

    expression = '"${' + ref + '}"'
    var = "$( python -c 'import sys; from pyscript import {}; print {}(sys.argv[1:])' {} )".format(BashClass.set_var_from_reference.__name__, BashClass.set_var_from_reference.__name__, expression)
    set_var = "echo -e \"${}\"".format(ref, enum.__name__)

    try:
      subprocess.run(var)
    except:
      exception_message = "Exception: Failed to get variable."
      print(exception_message)
      __init__()
      sys.exit(1)

    try:
      subprocess.run(set_var)
    except:
      exception_message = "Exception: Failed to set variable."
      print(exception_message)
      __init__()
      sys.exit(1)

class DomainListModel:
  command_prefix        = "sudo virsh"

  option_list_all       = "list --all"
  option_set_domain     = "--domain"
  option_set_target     = "--target"
  option_target_both    = "hybrid"
  option_target_disk    = "disk"
  option_target_memory  = "mem"

  state_paused    = "paused"
  state_started   = "running"
  state_stopped   = "shut off"
  state_stop      = "pmsuspended"

  def __init__(self, domain_list, domain_dict):
    self.domain_list = domain_list
    self.domain_dict = domain_dict

  def get_domain_status():
    if self.domain not in self.domain_list:
      syscall.exit(1)

    i = self.domain_list.index(self.domain)
    self.status = self.status_list(i)

  def get_lists():
    __get_domain_list()
    __get_domain_dict()

  def __get_domain_list():
    list_ref = "_ARR_DOMAIN"
    get_domain_list = "{} {} {}".format(command_prefix, option_list_all, option_set_domain)
    set_ref = "declare -a {}=$( {} )".format(list_ref, get_domain_list)
    subprocess.run(set_ref)
    BashClass.get_enum_from_reference(list_ref)
    self.domain_list = BashClass.enum

    if self.domain_list is None:
      sys.exit(1)

  def __get_domain_dict():
    domain_ref = "_DOMAIN"
    element_ref = "_ELEMENT"
    get_domain_list = "{} {} {}".format(command_prefix, option_list_all, option_set_domain)
    get_messy_domain_and_state = "{} {} | grep '${}' | head -n 1 '".format(command_prefix, option_list_all, domain_ref)

    for domain in self.domain_list:
      set_domain = "declare -a {}=\"{}\"".format(domain_ref, domain)
      status = ""

      while True:
        index=2
        get_delimited_value = "| awk 'END {print $" + index + "}'"
        get_element = "declare {}=$( \"{}{}\" )".format(element_ref, get_messy_domain_and_state, get_delimited_value)
        subprocess.run(get_element)
        BashVarController.set_var_from_reference(element_ref)

        if BashVarController.var is None:
          break

        status.__add__("{} ".format(BashVarController.var))
        index.__add__(1)

      self.domain_dict.append([domain, status])

    if self.domain_dict is None:
      sys.exit(1)

class DomainController:
  option_start        = "start"
  option_hard_stop    = "shutdown"
  option_force_stop   = "destroy"
  option_power_start  = "dompmwakeup"
  option_power_stop   = "dompmsuspend"
  option_soft_start   = "resume"
  option_soft_stop    = "suspend"

  set_start_domain        = "{} {}".format(command_prefix,option_start)
  set_force_stop_domain   = "{} {}".format(command_prefix,option_force_stop)
  set_hard_stop_domain    = "{} {}".format(command_prefix,option_hard_stop)

  set_power_start_domain                    = "{} {}".format(command_prefix,option_power_start)
  set_power_stop_domain_to_disk             = "{} {} {} {}".format(command_prefix,option_set_target,option_target_disk,option_set_domain)
  set_power_stop_domain_to_disk_and_memory  = "{} {} {} {}".format(command_prefix,option_set_target,option_target_both,option_set_domain)
  set_power_stop_domain_to_memory           = "{} {} {} {}".format(command_prefix,option_set_target,option_target_memory,option_set_domain)

  set_soft_start_domain = "{} {}".format(command_prefix,option_soft_start)
  set_soft_stop_domain  = "{} {}".format(command_prefix,option_soft_stop)

  def __init__(self, domain, status):
    self.domain = domain
    self.status = status

  def do_start_domain():
    if self.status is not state_paused and self.status is not state_stopped:
      sys.exit(1)

    __run_command_with_domain(set_start_domain)

  def do_force_stop_domain():
    if self.status is state_started:
      sys.exit(1)

    __run_command_with_domain(set_force_stop_domain)

  def do_hard_stop_domain():
    if self.status is state_started:
      sys.exit(1)

    __run_command_with_domain(set_hard_stop_domain)

  def do_power_stop_domain_to_disk():
    if self.status is not state_started:
      sys.exit(1)

    __run_command_with_domain(set_power_stop_domain_to_disk)

  def do_power_stop_domain_to_disk_and_memory():
    if self.status is not state_started:
      sys.exit(1)

    __run_command_with_domain(set_power_stop_domain_to_disk_and_memory,)

  def do_power_stop_domain_to_memory():
    if self.status is not state_stopped:
      sys.exit(1)

    __run_command_with_domain(set_power_stop_domain_to_memory)

  def do_soft_stop_domain():
    if self.status is not state_paused and self.status is not state_started:
      sys.exit(1)

    __run_command_with_domain(set_soft_stop_domain)

  def __run_command_with_domain( command ):
    if self.domain is None:
      sys.exit(1)

    this_subprocess = "{} {}".format(command, self.domain)

    try:
      subprocess.run(this_subprocess)

    except:
      exception_message = "An exception occurred."
      print(exception_message)