package com.example.carrot_backend.item.application;

import com.example.carrot_backend.item.controller.dto.ItemCreateRequestDto;
import com.example.carrot_backend.item.controller.dto.ItemDetailResponse;
import com.example.carrot_backend.item.controller.dto.ItemListResponse;
import com.example.carrot_backend.item.controller.dto.ItemSearchCondDto;
import com.example.carrot_backend.item.domain.ItemEntity;
import com.example.carrot_backend.item.domain.ItemReader;
import com.example.carrot_backend.item.domain.ItemWriter;
import com.example.carrot_backend.item.infrastructure.mapper.ItemMapper;
import com.example.carrot_backend.user.domain.UserReader;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ItemService {

    // MyBatis를 쓰기 위한 mapper
    private final ItemMapper itemMapper;

    private final ItemReader itemReader;
    private final ItemWriter itemWriter;
    private final UserReader userReader;

    public List<ItemListResponse> getItems(ItemSearchCondDto itemSearchCondDto) {
        return itemMapper.findAll(itemSearchCondDto);
    }

    public ItemDetailResponse getItemDetail(Long itemId){
        var item = itemReader.getItemById(itemId)
                .orElseThrow(() -> new RuntimeException("상품이 없습니다."));

        return new ItemDetailResponse(item);
    }

    @Transactional
    public void createItem(String userEmail, ItemCreateRequestDto itemCreateRequestDto){
        var user = userReader.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("회원정보가 존재하지 않습니다."));

        var newItem = ItemEntity.builder()
                .seller(user)
                .title(itemCreateRequestDto.getTitle())
                .price(itemCreateRequestDto.getPrice())
                .content(itemCreateRequestDto.getContent())
                .region(itemCreateRequestDto.getRegion())
                .category(itemCreateRequestDto.getCategory())
                .thumbnailUrl(itemCreateRequestDto.getThumbnailUrl())
                .build();

        itemWriter.save(newItem);
    }


}

