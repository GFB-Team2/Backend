package com.example.carrot_backend.item.controller.dto;

import com.example.carrot_backend.item.domain.ItemEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ItemListResponse {

    private Long id;
    private String title;
    private Integer price;
    private String region;
    private String category;
    private String thumbnailUrl;
    private String createdAt;

    public static ItemListResponse from(ItemEntity item) {
        return ItemListResponse.builder()
                .id(item.getId())
                .title(item.getTitle())
                .price(item.getPrice())
                .region(item.getRegion())
                .category(item.getCategory())
                .thumbnailUrl(item.getThumbnailUrl())
                .createdAt(item.getCreatedAt().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")))
                .build();
    }

}
