package com.seuprojeto.resource;
import java.util.List;

import com.seuprojeto.DTO.AuxilioDTO;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.mapper.AuxilioMapper;
import com.seuprojeto.service.AuxilioService;

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

@Path("/auxilio")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AuxilioResource {

    @Inject
    AuxilioService auxilioService;

    @GET
    public List<Auxilio> listAll() {
        return auxilioService.listarAuxilios();
    }

    @GET
    @Path("/ativos")
    public List<Auxilio> listAtivos() {
        return auxilioService.listarAuxiliosAtivos();
    }

    @GET
    @Path("/{id}")
    public AuxilioDTO findById(@PathParam("id") Long id) {
        Auxilio auxilio = auxilioService.buscarPorId(id);
        if (auxilio == null) {
            throw new NotFoundException("Auxilio não encontrado");
        }
        return AuxilioMapper.toDTO(auxilio);
    }

    @POST
    @Transactional
    public AuxilioDTO create(AuxilioDTO dto) { // cria um auxilio
        Auxilio auxilio = new Auxilio();
        auxilio.titulo = dto.titulo;
        auxilio.descricao = dto.descricao;
        auxilio.ativo = dto.ativo;

        auxilioService.salvar(auxilio);
        return AuxilioMapper.toDTO(auxilio);
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public AuxilioDTO update(@PathParam("id") Long id, AuxilioDTO updated) {
        Auxilio auxilio = auxilioService.buscarPorId(id);
        if (auxilio == null) {
            throw new NotFoundException("Auxilio não encontrado");
        }

        auxilio.titulo = updated.titulo;
        auxilio.descricao = updated.descricao;
        auxilio.ativo = updated.ativo;

        return AuxilioMapper.toDTO(auxilio);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        boolean deleted = auxilioService.remover(id);
        if (!deleted) {
            throw new NotFoundException("Auxilio não encontrado");
        }
    }
}
