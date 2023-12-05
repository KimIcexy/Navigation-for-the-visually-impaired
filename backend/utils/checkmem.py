import torch
t = torch.cuda.get_device_properties(0).total_memory
r = torch.cuda.memory_reserved(0)
a = torch.cuda.memory_allocated(0)
f = r-a  # free inside reserved
f
torch.cuda.mem_get_info()
torch.rand(290000, 20000).cuda()
