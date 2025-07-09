package com.clinicavet.petcare.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.clinicavet.petcare.model.Pet;

public interface PetRepository extends JpaRepository<Pet, Long> {
}
