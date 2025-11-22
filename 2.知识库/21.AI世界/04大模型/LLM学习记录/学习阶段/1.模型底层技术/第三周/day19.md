情感分类任务中，
用 mask 完形填空代替分类问题 
- 预训练模型（如BERT）本就擅长完形填空（MLM任务），Prompt Learning利用了这一点，比直接添加分类头更高效。
 ```python
x = "电影剧情很无聊" # 负面评论 label = "neg" # 负面标签
prompt_info = get_prompt(x) 
 即prompt_info = {  'prompt': "总体上来说很[MASK]。电影剧情很无聊",  'mask_offset': 6 # [MASK]在字符串中的位置 # }
 ```	
