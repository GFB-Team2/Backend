package com.example.carrot_backend.item.controller.dto;

import lombok.*;

import java.util.List;

@Getter
@Setter
public class ItemSearchCondDto {
    private String keyword;
    private List<String> regions;
    private List<String> categories;
}
