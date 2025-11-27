package com.example.carrot_backend.item.controller.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ItemCreateRequestDto {

    @NotBlank
    private String title;

    @NotBlank
    private String content;

    @Min(value = 0, message = "최소 금액은 0원 입니다.")
    private Integer price;

    @NotBlank
    private String region;

    @NotBlank
    private String category;

    private String thumbnailUrl;

}
