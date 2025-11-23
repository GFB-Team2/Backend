package com.example.carrot_backend.item.application;

import com.example.carrot_backend.item.controller.dto.ItemDetailResponse;
import com.example.carrot_backend.item.controller.dto.ItemListResponse;
import com.example.carrot_backend.item.controller.dto.ItemSearchCondDto;
import com.example.carrot_backend.item.domain.ItemReader;
import com.example.carrot_backend.item.infrastructure.mapper.ItemMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ItemService {

    private final ItemMapper itemMapper;
    private final ItemReader itemReader;

    public List<ItemListResponse> getItems(ItemSearchCondDto itemSearchCondDto) {
        return itemMapper.findAll(itemSearchCondDto);
    }

    public ItemDetailResponse getItemDetail(Long itemId){
        var item = itemReader.getItemById(itemId)
                .orElseThrow(() -> new RuntimeException("상품이 없습니다."));

        return new ItemDetailResponse(item);
    }


}

