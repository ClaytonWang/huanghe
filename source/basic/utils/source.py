def source_convert(s: str):
    gpu_count = 0
    if s.startswith("GPU"):
        machine_type = "GPU"
        _, gpu_count, cpu_count, memory = s.split()
        gpu_count = gpu_count.split("*")[0]
        cpu_count = cpu_count.split("C")[0]
        memory = memory.split("G")[0]
    else:
        machine_type = "CPU"
        _, cpu_count, memory = s.split()
        cpu_count = cpu_count.split("C")[0]
        memory = memory.split("G")[0]
    return machine_type, gpu_count, cpu_count, memory