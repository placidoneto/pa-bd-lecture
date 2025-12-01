package com.seuprojeto.resource;

import java.util.List;

import com.seuprojeto.DTO.BeneficioDTO;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.Beneficio;
import com.seuprojeto.mapper.BeneficioMapper;
import com.seuprojeto.service.BeneficioService;    

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/beneficio")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class BeneficioResource {

    @Inject
    BeneficioService beneficioService;

    @GET
    public List<Beneficio> listAll() {
        return beneficioService.listarBeneficio();
    }

    @GET
    @Path("/ativos")
    public List<Beneficio> listAtivos() {
        return beneficioService.listarBeneficiosAtivos();
    }

    @GET
    @Path("/{id}")
    public BeneficioDTO findById(@PathParam("id") Long id) {
        Beneficio beneficio = beneficioService.buscarPorId(id);
        if (beneficio == null) {
            throw new NotFoundException("Beneficio não encontrado");
        }
        return BeneficioMapper.toDTO(beneficio);
    }

    @POST
    @Transactional
    public BeneficioDTO create(BeneficioDTO beneficiorequest) {
        Beneficio beneficio = new Beneficio();
        beneficio.nome = beneficiorequest.nome;
        beneficio.descricao = beneficiorequest.descricao;
        beneficio.ativo = beneficiorequest.ativo;
        Auxilio aux = new Auxilio();
        aux.id = beneficiorequest.auxilioId;    
        beneficio.auxilio = aux;

        beneficioService.salvar(beneficio);
        return BeneficioMapper.toDTO(beneficio);
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public BeneficioDTO update(@PathParam("id") Long id, BeneficioDTO updated) {
        Beneficio beneficio = beneficioService.buscarPorId(id);
        if (beneficio == null) {
            throw new NotFoundException("Beneficio não encontrado");
        }

        beneficio.nome = updated.nome;
        beneficio.descricao = updated.descricao;
        beneficio.ativo = updated.ativo;

        return BeneficioMapper.toDTO(beneficio);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        boolean deleted = beneficioService.remover(id);
        if (!deleted) {
            throw new NotFoundException("Beneficio não encontrado");
        }
    }
}
