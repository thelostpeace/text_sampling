import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertModel, AdamW, BertConfig, BertPreTrainedModel

class BertSentenceEncoder(BertPreTrainedModel):
    """
        Bert Pretrain Fine Tuning On Text Classification, add attention on all layer cls
    """
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.bert = BertModel(config)
        pass

    def forward(self, input_ids, attention_mask, token_type_ids=None, position_ids=None, head_mask=None, inputs_embeds=None, labels=None, output_attentions=None):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions
        )

        return outputs
