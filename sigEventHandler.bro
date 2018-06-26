@load base/utils/exec
@load-sigs ./sig

redef exit_only_after_terminate=T;

event signature_match(stage: signature_state, msg: string, data: string)
{
        ##print msg;
        local t= fmt("python3 /home/boschma/Documents/ddosdbRuleGenerator/send_to_attacker.py '%s'", msg);
        local cmd = Exec::Command($cmd=t);
        when (local res = Exec::run(cmd))
        {
                print msg;
        }
}