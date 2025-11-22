package com.example.carrot_backend.auth.domain;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@AllArgsConstructor
public class TokenDto {
    private String AccessToken;
    private String RefreshToken;
}
