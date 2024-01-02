#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 22:31:31 2023

@author: chingchen
"""


import os
import flac
import numpy as np
import matplotlib
import function_for_flac as fd
import matplotlib.pyplot as plt
#import flac_interpolate as fi


plt.rcParams["font.family"] = "Helvetica"
#---------------------------------- DO WHAT -----------------------------------
### pdf or png
png             = 0
pdf             = 0
fig8 = 0 # 8 snapshot
fig4 = 1 # 4 snapshot
#---------------------------------- SETTING -----------------------------------
path = '/home/jiching/geoflac/'
#path = '/scratch2/jiching/22winter/'
#path = '/scratch2/jiching/03model/'
#path = '/scratch2/jiching/22summer/'
path = '/scratch2/jiching/04model/'
path = '/Users/chingchen/Desktop/model/'
savepath='/scratch2/jiching/data/'
savepath = '/Users/chingchen/Desktop/data/'
figpath='/scratch2/jiching/figure/'
figpath = '/Users/chingchen/Desktop/figure/'
figpath = '/Users/chingchen/Desktop/FLAC_Works/Eclogite_flat_slab/'

xmin,xmax = 300,900
zmin,zmax = -150,10
model2 = 'Nazca_ab05'
#model2 = 'Nazca_a0702'
model1 = 'Nazca_aa15'
frame1 = 30
frame2 = 60
frame3 = 140
frame4 = 180
limit = 3.2e-4
limit2 = 3.2e-2
negative = -250
skip = (slice(None, None, 8))
depth1=150
scale=0.03


bwith = 4
fontsize=35
labelsize=30

#------------------------------------------------------------------------------
def plot_snapshot(frame):
    x,z = fl.read_mesh(frame)
    xtop,ztop = fd.get_topo(x,z)
    phase = fl.read_phase(frame)
    ele_x,ele_z = flac.elem_coord(x, z)
    temp = fl.read_temperature(frame)
    return x, z, ele_x, ele_z, phase, temp, ztop
def get_vis(frame):
    x,z = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(x, z)
    vis = fl.read_visc(frame)
    xtop,ztop = fd.get_topo(x,z)
    return x,z,ele_x,ele_z,vis,ztop
colors = ["#93CCB1","#550A35","#2554C7","#008B8B","#4CC552",
      "#2E8B57","#524B52","#D14309","#DC143C","#FF8C00",
      "#FF8C00","#455E45","#F9DB24","#c98f49","#525252",
      "#CD5C5C","#00FF00","#FFFF00","#7158FF"]
phase15= matplotlib.colors.ListedColormap(colors)
colors2=[
 '#C98F49', '#92C0DF', '#2553C7', '#FFFFFF', '#6495ED',
 '#2E8B57', '#524B52', '#9A32CD', '#6B8E23','#D4DBF4',
 '#D8BFD8','#999999','#F2C85B','#92C0DF','#999999',
 '#4CC552','#999999','#999999','#999999','#999999']
phase8= matplotlib.colors.ListedColormap(colors2)

def dynamics_pressure(frame):
    pre = -fl.read_pres(frame) *1e8
    ooone = pre.flatten()
    x,z = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(x, z)
    a,b=np.polyfit(pre[ele_z<-50],ele_z[ele_z<-50].flatten(),deg=1)
    fit=(ele_z.flatten()-b)/a
    dypre=(ooone-fit).reshape(len(pre),len(pre[0])) 
    return x,z,dypre
def oceanic_slab2(frame,x,z,phase,trench_index):
    phase_oceanic = 3
    phase_ecolgite = 13
    phase_oceanic_1 = 17
    phase_ecolgite_1 = 18
    ele_x, ele_z = flac.elem_coord(x, z)
    trench_ind = int(trench_index[frame-1])
    crust_x = np.zeros(len(ele_x))
    crust_z = np.zeros(len(ele_x))
    for j in range(trench_ind,len(ele_x)):
        ind_oceanic = (phase[j,:] == phase_oceanic) + (phase[j,:] == phase_ecolgite)+(phase[j,:] == phase_oceanic_1) + (phase[j,:] == phase_ecolgite_1)
        if True in ind_oceanic:
            kk = ele_z[j,ind_oceanic]
            xx = ele_x[j,ind_oceanic]
            if len(kk[kk<-15])==0:
                continue
            crust_x[j] = np.max(xx[kk<-15])
            crust_z[j] = np.max(kk[kk<-15])       
    return crust_x,crust_z

#------------------------------------------------------------------------------
if fig8:
    fig, (ax,ax2,ax3,ax4)= plt.subplots(4,2,figsize=(34,22))
    #----------------------------- FIG1 -----------------------------
    model = model1
    os.chdir(path+model)
    fl = flac.Flac()
    time=fl.time
    
    #----------------------------- FIG 1-1 -----------------------------    
    ax5 = ax[1] 
    ax = ax[0]
    frame = frame1
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    ck = plt.cm.get_cmap('RdBu_r')
    cbpre=ax.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    cax = plt.axes([0.945, 0.285, 0.01, 0.431])
    cc3=fig.colorbar(cbpre, ax=ax,cax=cax, ticks=np.array([-250., -100.,  0., 100.,  250.]))
    cc3.set_label(label='Dynamics Pressure (MPa)', size=35)
    cc3.ax.tick_params(labelsize=30)
    cc3.ax.yaxis.set_label_position('left')
    ax.contour(xt,-zt,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax.text(270,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    ax.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<700)
        if True in up :
            ax.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 1-2 -----------------------------    
    ax6 = ax2[1] 
    ax2 = ax2[0]
    frame = frame2
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax2.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax2.contour(xt,-zt,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax2.text(270,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    ax2.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax2.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<700)
        if True in up :
            ax2.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax2.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 1-3 -----------------------------
    ax7 = ax3[1] 
    ax3 = ax3[0]
    frame = frame3
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax3.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax3.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax3.text(270,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    ax3.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax3.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<700)
        if True in up :
            ax3.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax3.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 1-4 -----------------------------
    ax8 = ax4[1] 
    ax4 = ax4[0]
    frame = frame4
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax4.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax4.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax4.text(270,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    ax4.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax4.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<700)
        if True in up :
            ax4.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax4.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 2 -----------------------------
    model = model2
    os.chdir(path+model)
    fl = flac.Flac()
    time=fl.time
    #----------------------------- FIG 2-1-----------------------------
    frame = frame1
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax5.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax5.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax5.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax5.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<900)
        if True in up :
            ax5.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax5.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 2-2-----------------------------
    frame = frame2
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax6.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax6.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax6.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax6.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<900)
        if True in up :
            ax6.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax6.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 2-3 -----------------------------
    frame = frame3
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax7.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax7.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax7.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax7.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>700)*(temp[ii,:]>800)*(x[ii,:]<900)
        if True in up :
            ax7.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax7.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 2-4-----------------------------
    frame = frame4
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax8.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax8.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax8.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax8.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>800)*(temp[ii,:]>700)*(x[ii,:]<900)
        if True in up :
            ax8.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax8.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    # ---------------------- plot setting --------------------------
    xmajor_ticks=np.array([250,300,400,500,600,700,800,900,1000])
    
    ymajor_ticks = np.linspace(200,0,num=5)
    for aa in [ax,ax2,ax3,ax4,ax5,ax6,ax7,ax8]:
        aa.tick_params(labelsize=labelsize,width=3,length=15,right=True, top=True,direction='in')
        aa.set_aspect('equal')
        aa.set_yticks(ymajor_ticks)
        aa.set_ylabel('Depth (km)',fontsize=fontsize)
        aa.set_xticks(xmajor_ticks)
        aa.set_xlim(xmin,xmax)
        aa.set_ylim(-zmin,-zmax)
        for axis in ['top','bottom','left','right']:
            aa.spines[axis].set_linewidth(bwith)
    ax4.set_xlabel('Distance (km)',fontsize=fontsize)
    ax8.set_xlabel('Distance (km)',fontsize=fontsize)
    ax.set_title('P$_0$ = 100',fontsize=50)
    ax5.set_title('ridge = 11 km',fontsize=50)
    if png:
        fig.savefig(figpath+model+'frame_'+str(frame)+'_pressure_compare.png')
    if pdf:
        fig.savefig(figpath+'fig6v2.pdf')
#------------------------------------------------------------------------------
if fig4:
    frame1 = 60
    frame2 = 80
    frame3 = 60
    frame4 = 144
    fig, (ax,ax2)= plt.subplots(2,2,figsize=(34,11))
    #----------------------------- FIG1 -----------------------------
    model = model1
    os.chdir(path+model)
    fl = flac.Flac()
    time=fl.time
    
    #----------------------------- FIG 1-1 -----------------------------    
    ax5 = ax[1] 
    ax = ax[0]
    frame = frame1
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    ck = plt.cm.get_cmap('RdBu_r')
    cbpre=ax.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    cax = plt.axes([0.93, 0.145, 0.01, 0.71])
    cc3=fig.colorbar(cbpre, ax=ax,cax=cax, ticks=np.array([-250., -100.,  0., 100.,  250.]))
    cc3.set_label(label='Dynamics Pressure (MPa)', size=35)
    cc3.ax.tick_params(labelsize=30)
    cc3.ax.yaxis.set_label_position('left')
    ax.contour(xt,-zt,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax.text(320,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    ax.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<900)
        if True in up :
            ax.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 1-2 -----------------------------    
    ax6 = ax2[1] 
    ax2 = ax2[0]
    frame = frame2
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax2.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax2.contour(xt,-zt,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax2.text(320,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    ax2.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    #ax2.contour(ele_x,-ele_z,new_pre/1e6,colors='darkblue',levels =[negative], linewidths=6)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<900)
        if True in up :
            ax2.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax2.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 2 -----------------------------
    model = model2
    os.chdir(path+model)
    fl = flac.Flac()
    time=fl.time
    #----------------------------- FIG 2-1-----------------------------
    frame = frame3
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax5.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax5.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax5.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    ax5.text(320,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>500)*(temp[ii,:]>800)*(x[ii,:]<900)
        if True in up :
            ax5.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax5.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    #----------------------------- FIG 2-2-----------------------------
    frame = frame4
    xt,zt = fl.read_mesh(frame)
    ele_x,ele_z = flac.elem_coord(xt, zt)
    temp = fl.read_temperature(frame)
    magma = fl.read_fmagma(frame)
    area = fl.read_area(frame)
    #--------------------- pressure plotting -------------------------
    x,z,new_pre = dynamics_pressure(frame)
    new_pre = new_pre-np.median(new_pre)
    cbpre=ax6.pcolormesh(ele_x,-ele_z,new_pre/1e6,cmap=ck,vmin=-250, vmax=250,shading='gouraud')
    ax6.contour(x,-z,temp,colors='#696969',levels =[200,400,600,800,1000,1200],linewidths=3)
    ax6.contour(ele_x,-ele_z,magma,colors=['#6B8E23'],levels =[limit], linewidths=6)
    ax6.text(320,130,str(np.round(fl.time[frame-1],1))+' Myr',fontsize=fontsize)
    print(model,frame,area[new_pre/1e6<negative].sum()/1e6)
    #-------------------- velocity vector ---------------------------
    xvel,zvel = fl.read_vel(frame)
    phase = fl.read_phase(frame)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    crust_x,crust_z = oceanic_slab2(frame, x, z, phase, trench_index)
    nex = len(x)
    for ii in range(int(trench_index[frame-1]),nex-1,8):
        up= (z[ii,:]> crust_z[ii])*(z[ii,:]>-depth1)*(z[ii,:]<-50)*(temp[ii,:]>600)
        right=(x[ii,:]>700)*(temp[ii,:]>800)*(x[ii,:]<900)
        if True in up :
            ax6.quiver(x[ii,up][skip],-z[ii,up][skip],xvel[ii,up][skip],zvel[ii,up][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
        if True in right:
            ax6.quiver(x[ii,right][skip],-z[ii,right][skip],xvel[ii,right][skip],zvel[ii,right][skip],
                     scale_units='xy', scale=scale,headlength=5,headwidth=3)
    # ---------------------- plot setting --------------------------
    xmajor_ticks=np.array([250,300,400,500,600,700,800,900,1000])
    
    ymajor_ticks = np.linspace(200,0,num=5)
    for aa in [ax,ax2,ax5,ax6]:
        aa.tick_params(labelsize=labelsize,width=3,length=15,right=True, top=True,direction='in',pad=10)
        aa.set_aspect('equal')
        aa.set_yticks(ymajor_ticks)
        aa.set_ylabel('depth (km)',fontsize=fontsize)
        aa.set_xticks(xmajor_ticks)
        aa.set_xlim(xmin,xmax)
        aa.set_ylim(-zmin,-zmax)
        for axis in ['top','bottom','left','right']:
            aa.spines[axis].set_linewidth(bwith)
    ax2.set_xlabel('distance (km)',fontsize=fontsize)
    ax6.set_xlabel('distance (km)',fontsize=fontsize)
    ax.set_title('p$_0$ = 100 p$_r$',fontsize=fontsize+5)
    ax5.set_title('11 km oceanic crust',fontsize=fontsize+5)
    if png:
        fig.savefig(figpath+model+'frame_'+str(frame)+'_pressure_compare.png')
    if pdf:
        fig.savefig(figpath+'fig6bv3.pdf')