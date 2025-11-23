package com.example.carrot_backend.item.infrastructure.mapper;

import com.example.carrot_backend.item.controller.dto.ItemListResponse;
import com.example.carrot_backend.item.controller.dto.ItemSearchCondDto;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface ItemMapper {

    List<ItemListResponse> findAll(ItemSearchCondDto itemSearchCondDto);


}
